from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging import FileHandler, Formatter
from elasticsearch import Elasticsearch

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  moment.init_app(app)

  app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

  from fyyur.artist import bp as artist_bp
  app.register_blueprint(artist_bp)

  from fyyur.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  from fyyur.main import bp as main_bp
  app.register_blueprint(main_bp)

  from fyyur.show import bp as show_bp
  app.register_blueprint(show_bp)

  from fyyur.venue import bp as venue_bp
  app.register_blueprint(venue_bp)

  if app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger = logging.getLogger(__name__)
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

  return app

from fyyur import models