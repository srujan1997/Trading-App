from . import order_query
import json
from request_handler.request_handler import read_particular_order


@order_query.route("/query/<order_number>", methods=["GET"])
def query_order(order_number):
    """
    Description: Executed Order Details API for internal service communication(GET)
    :param order_number: string
    :return: API response (Flask response object)
    """
    ord_arr = read_particular_order(order_number)
    json_data = json.dumps(ord_arr)
    return json_data
