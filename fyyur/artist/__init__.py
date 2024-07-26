from flask import Blueprint

bp = Blueprint('artist', __name__)

from fyyur.artist import routes, forms