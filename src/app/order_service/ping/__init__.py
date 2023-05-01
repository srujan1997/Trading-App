from flask import Blueprint

ping = Blueprint("ping", __name__)
from . import views
