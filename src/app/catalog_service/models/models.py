import enum
import json


class StockStatus(enum.Enum):
    active = 0
    suspended = 1


# Defining a catalog of the stocks required
catalog = {}


def load_catalog():
    global catalog
    catalog = json.load(open('./models/catalog_init.json', 'r'))


def initialise_stock_quantity(quantity_dict) -> None:
    global catalog
    for stock, quantity in quantity_dict:
        catalog[stock]["quantity"] = quantity if quantity > -1 else 0


# Defining the lookup method
def lookup(stock_name):
    stock_details = catalog.get(stock_name, None)
    if not stock_details:
        return -1, {}
    return (1, stock_details) if stock_details["status"] is StockStatus.active.value else (0, {})


# Defining the trade method
def trade(stock_name, n, trade_type, lock) -> int:
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
    else:
        stock_details["quantity"] -= n
    output = open('../output.json', 'w')
    json.dump(catalog, output)
    output.close()
    lock.release()
    return 1
