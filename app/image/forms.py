from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

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
    submit = SubmitField('Submit')
