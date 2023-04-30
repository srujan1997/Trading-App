from threading import Lock

from request_handler.catalog_handler_pb2 import LookupResponse, TradeResponse
from request_handler.catalog_handler_pb2_grpc import CatalogHandlerServicer
from models.models import lookup, trade


class CatalogHandlerServicer(CatalogHandlerServicer):
    """Provides methods that implement functionality of request handler server."""

    def __init__(self):
        self._lock = Lock()

    # Defining lookup for request handler server
    def Lookup(self, request, context):
        success, details = lookup(request.stock_name)
        return LookupResponse(success=success, stock_details=details)

    # Defining trade for request handler server
    def Trade(self, request, context):
        success = trade(request.stock_name, request.trade_volume, request.type, self._lock)
        return TradeResponse(success=success)
