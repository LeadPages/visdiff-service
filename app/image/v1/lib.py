import math
from PIL import Image, ImageColor
from ..image_lib import is_file, load_image, get_output_image_size,\
                        image_blender, get_diff_percent


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
                    diff_pixels[i, j] = ImageColor.getcolor('yellow',
                                                            IMAGE_ONE.mode)
                    diff_count += 1
                else:
                    # write a black pixel to the diffrence mask
                    diff_pixels[i, j] = ImageColor.getcolor('black',
                                                            IMAGE_ONE.mode)

    diff_percent = get_diff_percent(diff_count, response["outputSize"])

    if create_diff_file:
        response['outputImage'] = image_blender(IMAGE_ONE, IMAGE_TWO,
                                                diff_image, diff_count)
    else:
        response["outputImage"] = None

    # it is up to whatever consumes this output to determine whether the
    # calculated diff percentage or count of different
    # pixels is acceptible or not
    response['diffCount'] = diff_count
    response['diffPercent'] = diff_percent
    return response


def is_masked(pixel):
    if pixel[0] in range(245, 260) and pixel[1] in range(0, 4)\
            and pixel[2] in range(250, 260):
        return True
    else:
        return False


def pixels_are_different(pixel1, pixel2):
    """
    decide if the RGB components of the argument pixels match within the
    diff threshold this method is necessary to allow for the threshold to be
    configurable
    pixel1 - tuple(R, G, B) where R/G/B are 0 - 255
    pixel2 - tuple(R, G, B) where R/G/B are 0 - 255
    """
    # global DIFF_THRESHOLD
    DIFF_THRESHOLD = 40
    for component in range(3):
        if math.fabs(pixel1[component] - pixel2[component]) > DIFF_THRESHOLD:
            return True

    return False
