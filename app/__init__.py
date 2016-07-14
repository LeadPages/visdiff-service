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

    from .image.v1 import image as v1_image_blueprint
    app.register_blueprint(v1_image_blueprint, url_prefix='/image/v1')

    from .image.v2 import image as v2_image_blueprint
    app.register_blueprint(v2_image_blueprint, url_prefix='/image/v2')

    return app
