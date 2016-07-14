from PIL import Image, ImageChops
import io
import os
import math
import base64
import cStringIO
import numpy as np

RGB_BLACK = (0, 0, 0)
RGBA_BLACK = (0, 0, 0, 0)
RGB_YELLOW = (128, 128, 0)


def generate_difference_report(image_one, image_two,
                               create_diff_file=False):
    response = {}
    response['images'] = []

    if is_file(image_one) and is_file(image_two):
        response['images'].append({'location': image_one})
        response['images'].append({'location': image_two})
    else:
        response['images'].append({'location': 'base64string'})
        response['images'].append({'location': 'base64string'})

    IMAGE_ONE = load_image(image_one)
    IMAGE_TWO = load_image(image_two)

    response['images'][0]['size'] = IMAGE_ONE.size
    response['images'][1]['size'] = IMAGE_TWO.size

    response['outputSize'] = get_output_image_size(IMAGE_ONE, IMAGE_TWO)

    response['images'][0]['mode'] = IMAGE_ONE.mode
    response['images'][1]['mode'] = IMAGE_TWO.mode

    if IMAGE_ONE.mode == "RGB":
        diff_image = Image.new('RGB', response['outputSize'])
    else:
        diff_image = Image.new('RGBA', response['outputSize'])

    image1_pixels = IMAGE_ONE.load()
    image2_pixels = IMAGE_TWO.load()
    diff_pixels = diff_image.load()

    # iterate through the pixels of both images and compare, if different,
    # mark the difference image with yellow so it is noticeable to humans
    diff_count = 0
    diff_percent = 0.0
    for i in range(response['outputSize'][0] - 1):
        for j in range(response['outputSize'][1] - 1):
            if not is_masked(image1_pixels[i, j]):
                if pixels_are_different(image1_pixels[i, j],
                                        image2_pixels[i, j]):
                    # write a yellow pixel to the difference mask and
                    # increment difference count
                    diff_pixels[i, j] = (128, 128, 0)
                    diff_count += 1
                else:
                    # write a black pixel to the diffrence mask
                    diff_pixels[i, j] = (0, 0, 0)

    diff_percent = (float(diff_count)/(response['outputSize'][0] *
                                       response['outputSize'][1]))*100

    if create_diff_file:
        # do not blend if images are found to match because blending
        # can be expensive
        if diff_count != 0:
            # overlay the two input images, then overlay the yellow/black
            # marked
            # difference image to generate the output image that a human can
            # see
            final_image = Image.blend(IMAGE_ONE, IMAGE_TWO, 0.5)
            final_image = Image.blend(diff_image, final_image, 0.25)
            buffer = cStringIO.StringIO()
            final_image.save(buffer, format="PNG")
            response['outputImage'] = base64.b64encode(buffer.getvalue())
        else:
            final_image = Image.blend(IMAGE_ONE, diff_image, 0.25)
            buffer = cStringIO.StringIO()
            final_image.save(buffer, format="PNG")
            response['outputImage'] = base64.b64encode(buffer.getvalue())

    # it is up to whatever consumes this output to determine whether the
    # calculated diff percentage or count of different
    # pixels is acceptible or not
    response['diffCount'] = diff_count
    response['diffPercent'] = diff_percent
    return response


def generate_difference_report_v2(image_one, image_two,
                                  create_diff_file=False):
    response = {}
    response['images'] = []

    if is_file(image_one) and is_file(image_two):
        response['images'].append({'location': image_one})
        response['images'].append({'location': image_two})
    else:
        response['images'].append({'location': 'base64string'})
        response['images'].append({'location': 'base64string'})

    IMAGE_ONE = load_image(image_one)
    IMAGE_TWO = load_image(image_two)

    response['images'][0]['size'] = IMAGE_ONE.size
    response['images'][1]['size'] = IMAGE_TWO.size

    response['outputSize'] = get_output_image_size(IMAGE_ONE, IMAGE_TWO)

    response['images'][0]['mode'] = IMAGE_ONE.mode
    response['images'][1]['mode'] = IMAGE_TWO.mode

    # iterate through the pixels of both images and compare, if different,
    # mark the difference image with yellow so it is noticeable to humans
    diff_count = 0
    diff_percent = 0.0

    diff_image = Image.fromarray(np.zeros_like(IMAGE_ONE, dtype=np.uint8()), IMAGE_ONE.mode)


    diff_arr = np.subtract(np.asarray(IMAGE_ONE, dtype=np.uint8()), np.asarray(IMAGE_TWO, dtype=np.uint8()))
    diff_count = np.sum(np.any(diff_arr != np.array((0, 0, 0, 0)), axis=2))

    # diff_arr.argwhere

    # for i in range(response['outputSize'][0] - 1):
    #     for j in range(response['outputSize'][1] - 1):
    #         if not is_masked(IMAGE_ONE.getpixel((i, j))):
    #             if pixels_are_different(IMAGE_ONE.getpixel((i, j)),
    #                                     IMAGE_TWO.getpixel((i, j))):
    #                 # write a yellow pixel to the difference mask and
    #                 # increment difference count
    #                 diff_image.putpixel((i, j), (128, 128, 0))

    diff_percent = (float(diff_count)/(response['outputSize'][0] *
                                       response['outputSize'][1]))*100

    if create_diff_file:
        # do not blend if images are found to match because blending
        # can be expensive
        if diff_count != 0:
            # overlay the two input images, then overlay the yellow/black
            # marked
            # difference image to generate the output image that a human can
            # see
            final_image = Image.blend(IMAGE_ONE, IMAGE_TWO, 0.5)
            final_image = Image.blend(diff_image, final_image, 0.25)
            buffer = cStringIO.StringIO()
            final_image.save(buffer, format="PNG")
            response['outputImage'] = base64.b64encode(buffer.getvalue())
        else:
            final_image = Image.blend(IMAGE_ONE, diff_image, 0.25)
            buffer = cStringIO.StringIO()
            final_image.save(buffer, format="PNG")
            response['outputImage'] = base64.b64encode(buffer.getvalue())

    # it is up to whatever consumes this output to determine whether the
    # calculated diff percentage or count of different
    # pixels is acceptible or not
    response['diffCount'] = diff_count
    response['diffPercent'] = diff_percent
    return response


def is_file(path):
    """Checks to see if given path is valid"""
    return os.path.exists(os.path.dirname(path))


def load_image(image):
    """Loads the given image."""
    if not is_file(image):
        image = io.BytesIO(image.decode('base64'))
    return Image.open(image)


def is_masked(pixel):
    if pixel[0] in range(245, 260) and pixel[1] in range(0, 4)\
            and pixel[2] in range(250, 260):
        return True
    else:
        return False


def get_output_image_size(image_one, image_two):
    if image_one.size[0] > image_two.size[0]:
        output_width = image_one.size[0]
    else:
        output_width = image_two.size[0]

    if image_one.size[1] > image_two.size[1]:
        output_height = image_one.size[1]
    else:
        output_height = image_two.size[1]
    return (output_width, output_height)


def pixels_are_different(pixel1, pixel2):
    """
    decide if the RGB components of the argument pixels match within the
    diff threshold this method is necessary to allow for the threshold to be
    configurable
    pixel1 - tuple(R, G, B) where R/G/B are 0 - 255
    pixel2 - tuple(R, G, B) where R/G/B are 0 - 255
    """
    # global DIFF_THRESHOLD
    DIFF_THRESHOLD = 0
    for component in range(3):
        if math.fabs(pixel1[component] - pixel2[component]) > DIFF_THRESHOLD:
            return True

    return False
