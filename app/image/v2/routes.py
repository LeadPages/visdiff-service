from flask import jsonify, request
from . import image
from lib import generate_difference_report, get_boolean


@image.route("/api/diff/", methods=['POST'])
def image_diff_endpoint():
    images = request.form.getlist('images')

    threshold = request.form.get('threshold', default=0, type=int)
    output = get_boolean(request.form.get('returnOutputImage',
                                          default='false', type=str))
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(generate_difference_report(images[0],
                                              images[1],
                                              create_diff_file=output,
                                              diff_threshold=threshold)), 200
