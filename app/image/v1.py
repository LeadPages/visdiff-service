from flask import jsonify, request
from . import image
from .. import image_diff


@image.route("/api/v1/diff/", methods=['POST'])
def image_diff_endpoint_v1():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(image_diff.generate_difference_report(images[0],
                                                         images[1])), 200
