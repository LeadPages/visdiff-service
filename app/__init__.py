"""Initialization script for the application."""
from flask import Flask
from config import config


def create_app(config_name):
    """app factory function."""
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')

    return app
