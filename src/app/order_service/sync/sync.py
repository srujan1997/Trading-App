import requests
import socket
import csv
import os
from flask import current_app as app

from request_handler.request_handler import get_last_txn_id, set_last_txn_id, get_new_transaction_data
from cache import get_from_redis


def check_and_sync_db(leader):
    current_leader = app.leader_id
    new_leader = leader
    working_replica_id = list(set(['1', '2', '3']) - set([current_leader, new_leader]))[0]
    last_txn_id = get_from_redis("transaction_id")
    last_txn_id_local = get_last_txn_id()
    if last_txn_id == last_txn_id_local:
        return
    port_map = {"1": "6298",
                "2": "7298",
                "3": "8298"}
    ip = socket.gethostbyname(f"order_service_{working_replica_id}")
    url = f"http://{ip}:{port_map.get(working_replica_id)}/api/order_service/sync/sync_db"
    params = {"txn_id": last_txn_id_local}
    response = requests.get(url, params=params)
    data = response.json()
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
    writer = csv.writer(log_file)
    for row in data:
        temp = row.strip().split(",")
        writer.writerow(temp)
    log_file.close()
    set_last_txn_id(int(temp[0]))


def replicate_db_txn(data):
    _id = os.environ.get("ID")
    log_file = open(f"transaction_log_{_id}.csv", "a+", encoding='UTF8', newline='')
    writer = csv.writer(log_file)
    writer.writerow(data)
    log_file.close()
    return 1

