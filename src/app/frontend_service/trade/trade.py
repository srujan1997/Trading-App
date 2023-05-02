import os
import grpc
import socket

from trade import catalog_handler_pb2
from trade import catalog_handler_pb2_grpc
from trade import order_handler_pb2
from trade import order_handler_pb2_grpc
from cache import get_dict_redis, set_dict_redis


def lookup(stock_name):
    stock_details = get_dict_redis(stock_name)
    if stock_details:
        return (1, stock_details) if stock_details["status"] == 0 else (0, stock_details)
    host_ip = os.environ.get("HOST_IP", "localhost")
    hostname = os.environ.get("CATALOG_SERVICE", host_ip)
    ip = socket.gethostbyname(hostname)
    port = '5297'
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
        response = stub.Lookup(catalog_handler_pb2.LookupRequest(stock_name=stock_name))
    if response.success != -1:
        set_dict_redis(stock_name, dict(response.stock_details), 3 * 60)
    return response.success, dict(response.stock_details)


def order(stock_name, volume, trade_type):
    host_ip = os.environ.get("HOST_IP", "localhost")
    hostname = os.environ.get("ORDER_SERVICE", host_ip)
    ip = socket.gethostbyname(hostname)
    port = '6297'
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = order_handler_pb2_grpc.OrderHandlerStub(channel)
        response = stub.Order(order_handler_pb2.Request(stock_name=stock_name,trade_volume=volume, type=trade_type))
    return response.success, response.transaction_id

def get_order_details():
    pass
