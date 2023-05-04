from . import ping
from response import success_response


@ping.route("/", methods=["GET"])
def ping_service():
    # Order Service Ping API to check health.
    return success_response({"data": "pong"})
