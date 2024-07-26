from flask import Blueprint

bp = Blueprint('show', __name__)

from fyyur.show import routes, forms