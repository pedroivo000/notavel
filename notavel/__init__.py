from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion
from connexion.resolver import MethodViewResolver
from notavel.config import Config

# Globally accessible libraries:
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config=Config):
    """Generate configurable app instance"""
    connex_app = connexion.App(__name__, specification_dir="openapi")
    connex_app.add_api("notavel-api.yml", resolver=MethodViewResolver("notavel.views"))

    # Get the underlying flask app instance from connex_app:
    app = connex_app.app
    app.config.from_object(config())

    # Initialize plugins:
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():

        db.create_all()

    return app
