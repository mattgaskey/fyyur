from flask import Blueprint

bp = Blueprint('main', __name__)

from fyyur.main import routes, forms