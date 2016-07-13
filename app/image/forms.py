from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

# TODO file allowed
class ImageSubmitForm(Form):
    image_one = FileField('What is your base image?', validators=[
        FileRequired(),
    ])
    image_two = FileField('What is the image you want to compare?',
                          validators=[
                                        FileRequired()
                                    ])
    submit = SubmitField('Submit')
