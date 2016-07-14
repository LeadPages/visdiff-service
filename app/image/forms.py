from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, RadioField

# TODO gif support?
images = tuple('jpg jpe jpeg png svg bmp'.split())


class ImageSubmitForm(Form):
    image_one = FileField('What is your base image?', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])
    image_two = FileField('What is the image you want to compare?',
                          validators=[
                                        FileRequired(),
                                        FileAllowed(images, 'Images only!')
                                    ])
    version_radio_button = RadioField('API Version',
                                      choices=[('v1', 'Version 1 api'),
                                               ('v2', 'Version 2 api')],
                                      default='v1')
    submit = SubmitField('Submit')
