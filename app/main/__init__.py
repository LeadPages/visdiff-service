from flask import Blueprint

main = Blueprint('main', __name__)

# ignoring  E402, F401
from . import errors, diff  # noqa
