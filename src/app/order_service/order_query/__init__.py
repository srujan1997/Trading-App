from flask import Blueprint

order_query = Blueprint("order_query", __name__)
from . import views
