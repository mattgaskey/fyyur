from flask import render_template
from fyyur.main import bp

@bp.route('/')
def index():
    return render_template('pages/home.html')