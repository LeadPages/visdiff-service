from flask import jsonify, request
from . import image
from lib import generate_difference_report


@image.route("/api/diff/", methods=['POST'])
def image_diff_endpoint():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(generate_difference_report(images[0],
                                              images[1])), 200
