from . import ping
from response import success_response


@ping.route("/", methods=["GET"])
def ping_service():
    return success_response({"data": "pong"})


@ping.route("/leader", methods=["GET"])
def get_leader():
    from flask import current_app as app
    return success_response(app.leader_id)