from flask import redirect, url_for
from . import index


@index.route('/')
def index_page():
    return redirect(url_for('image.image_diff_test_page')), 302