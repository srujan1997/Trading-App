from flask import request
from flask import current_app as app

from . import sync
from response import success_response


@sync.route("/notify/leader", methods=["PUT"])
def notify_leader():
    req_dict = request.json
    new_leader = req_dict.get("leader_id")

    from sync.sync import check_and_sync_db
    from cache import get_from_redis
    leader_id = get_from_redis("leader_id")
    if leader_id == new_leader:
        return success_response("No new information recorded")

    if app.config["SERVICE_ID"] == new_leader:
        check_and_sync_db(new_leader)
    return success_response("Information received")


@sync.route("/sync_db", methods=["GET"])
def synchronize_transactions():
    req_dict = request.json

    from request_handler.request_handler import get_new_transaction_data
    data = get_new_transaction_data(req_dict["txn_id"])
    return success_response(data)


@sync.route("/replicate_db", methods=["POST"])
def replicate_transactions():
    req_dict = request.json

    from sync.sync import replicate_db_txn
    res = replicate_db_txn(req_dict["data"])

    return success_response(res)
