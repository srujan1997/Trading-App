from threading import Lock

from request_handler.catalog_handler_pb2 import LookupResponse, TradeResponse
from request_handler.catalog_handler_pb2_grpc import CatalogHandlerServicer
from models.models import lookup, trade


class CatalogHandlerServicer(CatalogHandlerServicer):
    """Provides methods that implement functionality of request handler server."""

    def __init__(self):
        self._lock = Lock()

    def Lookup(self, request, context):
        """
        Description: Defining lookup for request handler server
        :param request: lookup request (defined in proto)
        :param context:
        :return: lookup response (defined in proto)
        """
        success, details = lookup(request.stock_name)
        return LookupResponse(success=success, stock_details=details)

    def Trade(self, request, context):
        """
        Description: Defining trade for request handler server
        :param request: trade request (defined in proto)
        :param context:
        :return: trade response (defined in proto)
        """
        success = trade(request.stock_name, request.trade_volume, request.type, self._lock)
        return TradeResponse(success=success)
