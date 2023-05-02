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
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
    data = [txn_id, stock_name, trade_type, quantity]
    writer = csv.writer(log_file)
    writer.writerow(data)
    log_file.close()


def get_new_transaction_data(transaction_id):
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "r+", encoding='UTF8', newline='')
    data = log_file.readlines()
    return data[transaction_id+1:]


def get_last_txn_id():
    _id = os.environ.get("ID")
    if not os.path.isfile(f"transaction_log_{_id}.csv"):
        log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
        headers = ["transaction_id", "stock_name", "trade_type", "quantity"]
        writer = csv.writer(log_file)
        writer.writerow(headers)
        txn_id = 0
    else:
        log_file = open(f"transaction_log_{_id}.csv", "r+", encoding='UTF8', newline='')
        data = log_file.readlines()
        if len(data) == 1:
            txn_id = 0
        elif len(data) == 0:
            headers = ["transaction_id", "stock_name", "trade_type", "quantity"]
            writer = csv.writer(log_file)
            writer.writerow(headers)
            txn_id = 0
        else:
            txn_id = int(data[-1][0])
    log_file.close()
    return txn_id


def send_txn_to_replicas(data):
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
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/sync/replicate_db"
        body = {"data": data}
        response = requests.post(url, json=body)

    return True


# Helper function to process the order
def process_order(stock_name, volume, trade_type):
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
            # set_in_redis("transaction_id", txn_id)
            send_txn_to_replicas([txn_id, stock_name, trade_type, volume])
        return response.success, txn_id
    else:
        return response.success, -1

def read_particular_order(order_number):
    log_array = []
    _id = os.environ.get("ID")
    try:
        with open(f"transaction_log_{_id}.csv", "r", encoding='UTF8', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                log_array.append(row)
        return log_array[int(order_number)+1]
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
