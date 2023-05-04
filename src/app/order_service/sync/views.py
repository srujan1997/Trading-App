from flask import request

from . import sync
from response import success_response


@sync.route("/notify/leader", methods=["PUT"])
def notify_leader():
    """
    Desscription: API to notify elected leader to order service.
    :return: API response (Flask response object)
    """
    req_dict = request.json
    new_leader = req_dict.get("leader_id")

    from sync.sync import check_and_sync_db
    from cache import get_from_redis
    leader_id = get_from_redis("leader_id")
    if leader_id == new_leader:
        return success_response("No new information recorded")

    check_and_sync_db()
    return success_response("Information received")


@sync.route("/sync_db", methods=["GET"])
def synchronize_transactions():
    """
    Description: Helper API to synchronize databases between replicas.
    :return: API response (Flask response object)
    """
    req_dict = request.json

    from request_handler.request_handler import get_new_transaction_data
    data = get_new_transaction_data(req_dict["txn_id"])
    return success_response(data)


@sync.route("/last_transaction", methods=["GET"])
def last_transaction_id():
    """
    Description: API to get last transaction id from the service local database.
    :return: API response (Flask response object)
    """
    from request_handler.request_handler import get_last_txn_id
    return success_response(get_last_txn_id())


@sync.route("/replicate_transaction", methods=["POST"])
def replicate_transactions():
    """
    Description: Helper API to synchronize successful order log with healthy replicas.
    :return: API response (Flask response object)
    """
    req_dict = request.json

    from sync.sync import replicate_db_txn
    res = replicate_db_txn(req_dict["data"])

    return success_response(res)
