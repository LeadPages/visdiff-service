from flask import jsonify, request
from . import main
from .. import image_diff


@main.route("/visdiff/", methods=['GET', 'POST'])
def image_diff_endpoint():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(image_diff.generate_difference_report(images[0], images[1])), 200
