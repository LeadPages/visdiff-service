from flask import Blueprint

index = Blueprint('index', __name__)

# ignoring  E402, F401
from . import routes  # noqa
