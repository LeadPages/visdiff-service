from flask import jsonify, request, render_template
from . import image
from .. import image_diff


@image.route("/api/v1/diff/", methods=['POST'])
def image_diff_endpoint_v1():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(image_diff.generate_difference_report(images[0],
                                                         images[1])), 200

@image.route("/diff/")
def image_diff_test_page():
    return render_template("diff_comparision.html"), 200


@image.route("/contains/")
def image_contains_test_page():
    return render_template("diff_contains.html"), 200
