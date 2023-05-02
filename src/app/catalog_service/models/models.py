import enum
import json
import os

from cache import delete_from_redis


class StockStatus(enum.Enum):
    # Enum to tag status of a stock
    active = 0
    suspended = 1


# Defining a catalog of the stocks required
catalog = {}


def load_catalog():
    """
    Description: Function to read the state of the catalog on startup.
    :return: -
    """
    global catalog
    if os.path.getsize('./output.json') > 0:
        catalog = json.load(open('./output.json', 'r'))
    else:
        catalog = json.load(open('./models/catalog_init.json', 'r'))


def initialise_stock_quantity(quantity_dict) -> None:
    """
    Description: Function to take initialise the catalog inmemory dict.
    :param quantity_dict: dict
    :return: -
    """
    global catalog
    for stock, quantity in quantity_dict:
        catalog[stock]["quantity"] = quantity if quantity > -1 else 0


def lookup(stock_name):
    """
    Description: Function for stock lookup.
    :param stock_name:  String
    :return: Tuple of (query_success(int), stock_details(dict))
    """
    stock_details = catalog.get(stock_name, None)
    if not stock_details:
        return -1, {}
    return (1, stock_details) if stock_details["status"] is StockStatus.active.value else (0, stock_details)


def trade(stock_name, n, trade_type, lock) -> int:
    """
    Description: The trade method
    :param stock_name: string
    :param n: int
    :param trade_type: string
    :param lock: threading lock
    :return: trade_success(int)
    """
    if n <= 0:
        return 0
    stock_lookup, _ = lookup(stock_name)
    if stock_lookup == -1 or stock_lookup == 0:
        return stock_lookup
    lock.acquire()
    stock_details = catalog[stock_name]
    if n > stock_details["quantity"]:
        return -2
    if trade_type == "sell":
        stock_details["quantity"] += n
    elif trade_type == "buy":
        stock_details["quantity"] -= n
    output = open('../catalog_service/output.json', 'w')
    json.dump(catalog, output)
    output.close()
    delete_from_redis(stock_name)
    lock.release()
    return 1
