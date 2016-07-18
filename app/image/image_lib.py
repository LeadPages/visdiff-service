from PIL import Image, ImageFile
import io
import os
import base64
import cStringIO

SUPPORTED_IMAGES = tuple('jpg jpe jpeg png bmp'.split())


def is_file(path):
    """Checks to see if given path is valid"""
    return os.path.exists(os.path.dirname(path))


def load_image(image):
    """Loads the given image."""
    if is_file(image):
        filename, file_extension = os.path.splitext(image)
        if file_extension.replace(".", "") in SUPPORTED_IMAGES:
            return Image.open(image)
        else:
            raise ValueError("Image type was not listed in supported images %s"
                             % (SUPPORTED_IMAGES, ))
    else:
        return Image.open(io.BytesIO(image.decode('base64')))


def get_output_image_size(image_one, image_two):
    if (issubclass(type(image_one), ImageFile.ImageFile)
            and issubclass(type(image_two), ImageFile.ImageFile)):
        if image_one.size[0] > image_two.size[0]:
            output_width = image_one.size[0]
        else:
            output_width = image_two.size[0]

        if image_one.size[1] > image_two.size[1]:
            output_height = image_one.size[1]
        else:
            output_height = image_two.size[1]
        return (output_width, output_height)
    else:
        raise ValueError("Both parameters must be of type Image")


def image_blender(image_one, image_two, diff_image, diff_count):
    """
    overlay the two input images, then overlay the yellow/black marked
    difference image to generate the output image that a human can see
    """
    if diff_count != 0:

        final_image = Image.blend(image_one, image_two, 0.5)
        final_image = Image.blend(diff_image, final_image, 0.25)
        buffer = cStringIO.StringIO()
        final_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())
    else:
        final_image = Image.blend(image_one, diff_image, 0.25)
        buffer = cStringIO.StringIO()
        final_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())


def get_diff_percent(diff_pixel_count, image_size):
    """Gets the percentage value from the difference count and the size of
        the image"""
    return (float(diff_pixel_count)/(image_size[0] *
                                     image_size[1]))*100
