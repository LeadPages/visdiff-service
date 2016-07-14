from flask import Blueprint

image = Blueprint('imagev2', __name__)

# ignoring  E402, F401
from . import routes  # noqa
