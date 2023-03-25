from threading import Lock

from request_handler.catalog_handler_pb2 import Response
from request_handler.catalog_handler_pb2_grpc import RequestHandlerServicer
from models.models import lookup, trade


class RequestHandlerServicer(RequestHandlerServicer):
    """Provides methods that implement functionality of request handler server."""

    def __init__(self):
        self._lock = Lock()

    # Defining lookup for request handler server
    def Lookup(self, request, context):
        res = lookup(request.stock_name)
        return Response(message=res)

    # Defining trade for request handler server
    def Trade(self, request, context):
        res = trade(request.stock_name, request.trade_volume, request.type, self._lock)
        return Response(message=res)
