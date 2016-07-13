from flask import jsonify, request, render_template
from . import image
from .. import image_diff
import base64
from .forms import ImageSubmitForm
from werkzeug.utils import secure_filename


@image.route("/api/v1/diff/", methods=['POST'])
def image_diff_endpoint_v1():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(image_diff.generate_difference_report(images[0],
                                                         images[1])), 200


@image.route("/diff/", methods=('GET', 'POST'))
def image_diff_test_page():
    form = ImageSubmitForm()
    if form.validate_on_submit():
        image_one_name = secure_filename(form.image_one.data.filename)
        image_two_name = secure_filename(form.image_two.data.filename)

        image_one_type = secure_filename(form.image_one.data.type)
        image_two_type = secure_filename(form.image_one.data.type)

        image_one = base64.b64encode(form.image_one.data.stream.read())
        image_two = base64.b64encode(form.image_two.data.stream.read())
        diff_report = image_diff.generate_difference_report(image_one,
                                                            image_two,
                                                            True)
        return render_template("comparison.html",
                               image_one=image_one,
                               image_two=image_two,
                               image_blend=diff_report["outputImage"]), 200
    return render_template("diff_comparision.html", form=form), 200


@image.route("/contains/")
def image_contains_test_page():
    return render_template("diff_contains.html"), 200
