import os
import socket
import requests

# HTTP service_ids and ports mapping.(default is used for running without containers. (ignore in production env))
port_map = {"1": "6298",
            "2": "7298",
            "3": "8298",
            "default": "6298"
            }


def get_leader_id():
    """
    Description: Method to find the elect leader in the ecosystem.
    :return: leader (string)
    """
    host_ip = os.environ.get("HOST_IP", "localhost")
    leader = -1
    for i in range(1, 4):
        hostname = f"{os.environ.get('ORDER_SERVICE', host_ip)}_{str(i)}"
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            continue
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/ping"
        response = requests.get(url)
        if response.status_code == 200 and i > leader:
            leader = i

    return str(leader)


def notify_leader(leader):
    """
    Description: Method to notify elected leader to other replicas.
    :param leader: string
    :return: True(Bool)
    """
    for i in range(1, 4):
        hostname = f"order_service_{i}"
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            continue
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/sync/notify/leader"
        body = {"leader_id": leader}
        response = requests.put(url, json=body)

    return True
