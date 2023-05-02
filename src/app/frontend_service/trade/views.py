from flask import request

from trade import trade
import error_codes
from response import success, bad_request, not_found


@trade.route("/order", methods=["POST"])
def order():
    """
        Order
        Required params:None
    """
    req_dict = request.json
    if req_dict is None:
        return bad_request(error_codes.PARAMETERS_MISSING, "Request body is missing")

    stock_name = req_dict.get("name", None)
    volume = req_dict.get("quantity", None)
    trade_type = req_dict.get("type", None)
    if (stock_name is None) or (volume is None) or (trade_type is None):
        return bad_request(error_codes.PARAMETERS_MISSING, "Parameter Missing")

    from trade.trade import order
    _, txn_id = order(stock_name, volume, trade_type)

    return bad_request() if txn_id == -1 else success({"transaction_number": txn_id})


@trade.route("/lookup", methods=["GET"])
def lookup():
    """
        Order lookup
        Required params:None
    """
    req_dict = request.json #check why request.args not working for params.
    stock_name = req_dict.get("name", None)
    if stock_name is None:
        return bad_request(error_codes.PARAMETERS_MISSING, "Stock name is missing")

    from trade.trade import lookup
    flag, stock_details = lookup(stock_name)

    return not_found(error_text="Stock not found") if flag == -1 else success(stock_details)