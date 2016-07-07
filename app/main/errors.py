from flask import jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """
    404 error handler for entire application
    """
    return jsonify(message="an error has occured"), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """
    500 error handler for entire application
    """
    return jsonify(message="an error has occured"), 500
