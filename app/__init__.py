"""Initialization script for the application."""
from flask import Flask
from config import config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_name):
    """app factory function."""
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    # attach routes and custom error pages here
    from .image import image as image_blueprint
    app.register_blueprint(image_blueprint, url_prefix='/image')

    return app
