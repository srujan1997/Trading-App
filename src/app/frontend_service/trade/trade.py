import os
import grpc
import socket

from trade import catalog_handler_pb2
from trade import catalog_handler_pb2_grpc
from trade import order_handler_pb2
from trade import order_handler_pb2_grpc
from trade.leader import get_leader_id, notify_leader
import requests
from cache import get_dict_redis, set_dict_redis, get_from_redis, set_in_redis


def lookup(stock_name):
    """
    Description: Helper to handle lookup requests.
    :param stock_name: string
    :return: request_success, stock_details (Tuple(int, dict))
    """
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
    """
    Description: Helper to handle order requests.
    :param stock_name: string
    :param volume: int
    :param trade_type: string
    :return: request_success, stock_details (Tuple(int, string))
    """
    port_map = {"1": "6297",
                "2": "7297",
                "3": "8297",
                "default": "6297"}
    host_ip = os.environ.get("HOST_IP", "localhost")
    hostname = os.environ.get("ORDER_SERVICE", host_ip)
    leader_id = "default" if host_ip == "localhost" else get_from_redis("leader_id")
    if host_ip != "local_host":
        hostname += f"_{leader_id}"

    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        leader_id = get_leader_id()
        notify_leader(leader_id)
        set_in_redis("leader_id", leader_id)
        return order(stock_name, volume, trade_type)

    port = port_map.get(leader_id, "6297")
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = order_handler_pb2_grpc.OrderHandlerStub(channel)
        response = stub.Order(order_handler_pb2.Request(stock_name=stock_name, trade_volume=volume, type=trade_type))
    return response.success, response.transaction_id


def get_order_details(order_number):
    """
    Description: Helper to get order details from transaction_id.
    :param order_number: string
    :return: order_details (dict)
    """
    port_map = {"1": "6298",
                "2": "7298",
                "3": "8298",
                "default": "6298"}
    host_ip = os.environ.get("HOST_IP", "localhost")
    hostname = os.environ.get("ORDER_SERVICE", host_ip)
    leader_id = "default" if host_ip == "localhost" else get_from_redis("leader_id")
    if host_ip != "local_host":
        hostname += f"_{leader_id}"

    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        leader_id = get_leader_id()
        set_in_redis("leader_id", leader_id)
        return get_order_details(order_number)
    port = port_map.get(leader_id, "6298")
    url = f"http://{ip}:{port}/api/order_service/order_query/query/{order_number}"
    res = requests.get(url)
    return res.json()
