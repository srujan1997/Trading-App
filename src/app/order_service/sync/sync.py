import requests
import socket
import csv
import os

from request_handler.request_handler import get_last_txn_id, get_new_transaction_data
from cache import get_from_redis

# HTTP service_ids and ports mapping.
port_map = {"1": "6298",
            "2": "7298",
            "3": "8298"}


def check_and_sync_db():
    """
    Description: Helper to synchronise databases on new leader election.
    :return: -
    """
    last_txn_id = get_from_redis("transaction_id")
    last_txn_id_local = get_last_txn_id()
    if last_txn_id == last_txn_id_local:
        return
    replica_id = find_replica_to_sync(last_txn_id)
    # if replica_id:
    sync_db_with_replica(replica_id, last_txn_id_local)


def find_replica_to_sync(last_txn_id):
    """
    Description: Helper to find a replica to synchronise databases on new leader election.
    :param last_txn_id: string
    :return: replica_id(string or None)
    """
    # replica_id = None
    for i in range(1, 4):
        hostname = f"order_service_{i}"
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            continue
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/sync/last_transaction"
        response = requests.get(url)
        last_txn_id_replica = response.json()["data"]
        if last_txn_id_replica == last_txn_id:
            # replica_id = str(i)
            break
    return str(i)


def sync_db_with_replica(replica_id, txn_id):
    """
    Description: Helper to synchronise databases with replica on new leader election.
    :param replica_id: string
    :param txn_id: string
    :return: -
    """
    ip = socket.gethostbyname(f"order_service_{replica_id}")
    url = f"http://{ip}:{port_map.get(replica_id)}/api/order_service/sync/sync_db"
    body = {"txn_id": txn_id}
    response = requests.get(url, json=body)
    data = response.json()["data"]
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
    writer = csv.writer(log_file)
    for row in data:
        temp = row.strip().split(",")
        writer.writerow(temp)
    log_file.close()


def replicate_db_txn(data):
    """
    Description: Helper to propagate successful order details to healthy replicas.
    :param data:
    :return:
    """
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
    writer = csv.writer(log_file)
    writer.writerow(data)
    log_file.close()
    return 1
