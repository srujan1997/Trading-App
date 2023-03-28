import grpc
import csv
import os
from threading import Lock

from request_handler import order_handler_pb2
from request_handler import order_handler_pb2_grpc
from request_handler import catalog_handler_pb2
from request_handler import catalog_handler_pb2_grpc

txn_id = None
lock = Lock()


def log_transaction(txn_id, stock_name, trade_type, quantity):
    log_file = open("transaction_log.csv", "a", encoding='UTF8', newline='')
    data = [txn_id, stock_name, trade_type, quantity]
    writer = csv.writer(log_file)
    writer.writerow(data)
    log_file.close()


def get_last_txn_id():
    global txn_id
    if not os.path.isfile("transaction_log.csv"):
        log_file = open("transaction_log.csv", "w", encoding='UTF8', newline='')
        headers = ["transaction_id", "stock_name", "trade_type", "quantity"]
        writer = csv.writer(log_file)
        writer.writerow(headers)
        txn_id = 0
    else:
        log_file = open("transaction_log.csv", "r")
        data = log_file.readlines()
        txn_id = 0 if len(data)==1 else data[-1][0]
    log_file.close()


# Helper function to process the order
def process_order(stock_name, volume, trade_type):
    global txn_id, lock
    hostname = "172.17.0.2"
    port = '5297'
    with grpc.insecure_channel(hostname+':'+port) as channel:
        stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
        response = stub.Trade(catalog_handler_pb2.TradeRequest(stock_name=stock_name,
                                                               trade_volume=volume, type=trade_type))
    if response.success == 1:
        lock.acquire()
        log_transaction(txn_id, stock_name, trade_type, volume)
        txn_id += 1
        lock.release()
        return response.success, txn_id
    else:
        return response.success, -1


class OrderHandlerServicer(order_handler_pb2_grpc.OrderHandlerServicer):
    """Provides methods that implement functionality of request handler server."""

    def __init__(self):
        pass

    # Order definition for request handler of order service
    def Order(self, request, context):
        success, transaction_id = process_order(request.stock_name, request.trade_volume, request.type)
        return order_handler_pb2.Response(success=success, transaction_id=transaction_id)
