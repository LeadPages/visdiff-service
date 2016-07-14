from flask import Blueprint

image = Blueprint('image', __name__)

# ignoring  E402, F401
from . import routes, errors, v1, v2  # noqa
