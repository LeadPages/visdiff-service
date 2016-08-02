from flask import render_template
from . import image
from .v1.lib import generate_difference_report as generate_difference_report
from .v2.lib import generate_difference_report as generate_difference_report_v2
import base64
from .forms import ImageSubmitForm
from werkzeug.utils import secure_filename


@image.route("/diff/", methods=['GET', 'POST'])
def image_diff_test_page():
    form = ImageSubmitForm()
    if form.validate_on_submit():
        image_one_name = secure_filename(form.image_one.data.filename)
        image_two_name = secure_filename(form.image_two.data.filename)

        image_one = base64.b64encode(form.image_one.data.stream.read())
        image_two = base64.b64encode(form.image_two.data.stream.read())

        threshold = form.diff_threshold.data

        if form.version_radio_button.data == "v1":
            diff_report = generate_difference_report(image_one,
                                                     image_two,
                                                     True)
        else:
            diff_report = generate_difference_report_v2(image_one,
                                                        image_two,
                                                        True,
                                                        diff_threshold=
                                                        threshold)
        images = [
            dict(name=image_one_name, image=image_one),
            dict(name=image_two_name, image=image_two),
            dict(name='Comparison', image=diff_report['outputImage'])
        ]
        diff_report['outputImage'] = {}
        return render_template("comparison.html",
                               report=diff_report,
                               images=images,
                               engine=form.version_radio_button.data), 200
    return render_template("diff_comparision.html", form=form), 200
