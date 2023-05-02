import grpc
import csv
import os
from threading import Lock
import socket
import requests

from request_handler import order_handler_pb2
from request_handler import order_handler_pb2_grpc
from request_handler import catalog_handler_pb2
from request_handler import catalog_handler_pb2_grpc
from cache import set_in_redis, get_from_redis

lock = Lock()


def log_transaction(txn_id, stock_name, trade_type, quantity):
    """
    Description: Helper to log successful trades to database.
    :param txn_id: string
    :param stock_name: string
    :param trade_type: string
    :param quantity: float
    :return: -
    """
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
    data = [txn_id, stock_name, trade_type, quantity]
    writer = csv.writer(log_file)
    writer.writerow(data)
    log_file.close()


def get_new_transaction_data(transaction_id):
    """
    Description: Helper to retrieve all logs after the given transaction_id from database.
    :param transaction_id: string
    :return: data (List)
    """
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "r+", encoding='UTF8', newline='')
    data = log_file.readlines()
    return data[int(transaction_id):]


def get_last_txn_id():
    """
    Description: Helper to get last transaction id from the service database.
    :return: transaction_id (string)
    """
    _id = os.environ.get("ID")
    if not os.path.isfile(f"transaction_log_{_id}.csv"):
        log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
        txn_id = "0"
    else:
        log_file = open(f"transaction_log_{_id}.csv", "r+", encoding='UTF8', newline='')
        data = log_file.readlines()
        if len(data) == 0:
            txn_id = "0"
        else:
            txn_id = data[-1][0]
    log_file.close()
    return txn_id


def send_txn_to_replicas(data):
    """
    Description: Helper to send successful transactions to other replicas.
    :param data: list
    :return: True (Bool)
    """
    port_map = {"1": "6298",
                "2": "7298",
                "3": "8298",
                }
    leader = get_from_redis("leader_id")
    for i in range(1, 4):
        if i == int(leader):
            continue
        hostname = f"order_service_{i}"
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            continue
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/sync/replicate_transaction"
        body = {"data": data}
        response = requests.post(url, json=body)

    return True


def process_order(stock_name, volume, trade_type):
    """
    Description: Helper function to process the order.
    :param stock_name: string
    :param volume: float
    :param trade_type: string
    :return: order_success, transaction_id (Tuple(int, string))
    """
    global lock
    txn_id = int(get_from_redis("transaction_id"))
    host_ip = os.environ.get("HOST_IP", "localhost")
    hostname = os.environ.get("CATALOG_SERVICE", host_ip)
    ip = socket.gethostbyname(hostname)
    port = '5297'
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
        response = stub.Trade(catalog_handler_pb2.TradeRequest(stock_name=stock_name,
                                                               trade_volume=volume, type=trade_type))
    if response.success == 1:
        lock.acquire()
        txn_id += 1
        log_transaction(txn_id, stock_name, trade_type, volume)
        lock.release()
        if host_ip != "localhost":
            send_txn_to_replicas([txn_id, stock_name, trade_type, volume])
        return response.success, txn_id
    else:
        return response.success, -1


def read_particular_order(order_number):
    """
    Description: Helper to retrieve executed order details from transaction_id.
    :param order_number: string
    :return: order_details (dict)
    """
    log_array = []
    _id = os.environ.get("ID")
    try:
        with open(f"transaction_log_{_id}.csv", "r", encoding='UTF8', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                log_array.append(row)
        if(int(order_number)<1):
            return {}
        return log_array[int(order_number)-1]
    except IndexError:
        return {}


class OrderHandlerServicer(order_handler_pb2_grpc.OrderHandlerServicer):
    """Provides methods that implement functionality of request handler server."""

    def __init__(self):
        pass

    # Order definition for request handler of order service
    def Order(self, request, context):
        success, transaction_id = process_order(request.stock_name, request.trade_volume, request.type)
        return order_handler_pb2.Response(success=success, transaction_id=transaction_id)
