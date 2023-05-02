from . import ping
from response import success_response


@ping.route("/", methods=["GET"])
def ping_service():
    return success_response({"data": "pong"})
