from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging import FileHandler, Formatter
import os

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  moment.init_app(app)

  from fyyur.main import bp as main_bp
  app.register_blueprint(main_bp)

  from fyyur.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

  return app

from fyyur import models