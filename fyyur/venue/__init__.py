from flask import Blueprint

bp = Blueprint('venue', __name__)

from fyyur.venue import routes, forms