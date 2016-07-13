from flask import Blueprint

image = Blueprint('image', __name__)

# ignoring  E402, F401
from . import errors, v1  # noqa
