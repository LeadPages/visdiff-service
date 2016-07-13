from flask import jsonify, request
from . import image
from .. import image_diff


<<<<<<< 99375249a41b017dfe3a5c7a75a6e87478cab9dd
@image.route("/api/v1/diff/", methods=['POST'])
=======
@image.route("/api/v1/diff/", methods=['GET', 'POST'])
>>>>>>> rename complete
def image_diff_endpoint_v1():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(image_diff.generate_difference_report(images[0],
                                                         images[1])), 200
