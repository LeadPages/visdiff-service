from flask import jsonify, request, render_template
from . import image
from .. import image_diff
import base64
from .forms import ImageSubmitForm
from werkzeug.utils import secure_filename


@image.route("/api/v2/diff/", methods=['POST'])
def image_diff_endpoint_v2():
    images = request.form.getlist('images')
    if len(images) != 2:
        return jsonify(message="2 images must be specified"), 404
    return jsonify(image_diff.generate_difference_report_v2(images[0],
                                                            images[1])), 200


@image.route("/v2/diff/", methods=('GET', 'POST'))
def image_diff_test_page_v2():
    form = ImageSubmitForm()
    if form.validate_on_submit():
        image_one_name = secure_filename(form.image_one.data.filename)
        image_two_name = secure_filename(form.image_two.data.filename)

        # image_one_type = secure_filename(form.image_one.data.type)
        # image_two_type = secure_filename(form.image_one.data.type)

        image_one = base64.b64encode(form.image_one.data.stream.read())
        image_two = base64.b64encode(form.image_two.data.stream.read())
        diff_report = image_diff.generate_difference_report_v2(image_one,
                                                               image_two,
                                                               True)
        images = [
            dict(name=image_one_name, image=image_one),
            dict(name=image_two_name, image=image_two),
            dict(name='Comparison', image=diff_report['outputImage'])
        ]
        diff_report['outputImage'] = {}
        return render_template("comparison.html",
                               report=diff_report,
                               images=images), 200
    return render_template("diff_comparision.html", form=form), 200
