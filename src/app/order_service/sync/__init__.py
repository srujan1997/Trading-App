from flask import Blueprint

sync = Blueprint("sync", __name__)
from . import views
