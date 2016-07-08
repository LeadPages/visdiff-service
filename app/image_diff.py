from PIL import Image
import io
import math


def generate_difference_report_from_string(image_one, image_two,
                                           create_diff_file=False):
    response = {}
    response['images'] = []
    response['images'].append({'location': 'fromString'})
    response['images'].append({'location': 'fromString'})

    IMAGE_ONE = Image.open(io.BytesIO(image_one.decode('base64')))
    IMAGE_TWO = Image.open(io.BytesIO(image_two.decode('base64')))

    response['images'][0]['size'] = IMAGE_ONE.size
    response['images'][1]['size'] = IMAGE_TWO.size

    if IMAGE_ONE.size[0] > IMAGE_TWO.size[0]:
        output_width = IMAGE_ONE.size[0]
    else:
        output_width = IMAGE_TWO.size[0]

    if IMAGE_ONE.size[1] > IMAGE_TWO.size[1]:
        output_height = IMAGE_ONE.size[1]
    else:
        output_height = IMAGE_TWO.size[1]

    response['outputSize'] = (output_width, output_height)

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
    for i in range(output_width-1):
        for j in range(output_height-1):
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

    diff_percent = (float(diff_count)/(output_width * output_height))*100

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
            final_image.save(response['outputName'])
        else:
            final_image = Image.blend(IMAGE_ONE, diff_image, 0.25)
            final_image.save(response['outputName'])

    # it is up to whatever consumes this output to determine whether the
    # calculated diff percentage or count of different
    # pixels is acceptible or not
    response['diffCount'] = diff_count
    response['diffPercent'] = diff_percent
    return response


def generate_difference_report(image_one_path, image_two_path,
                               create_diff_file=False):
    response = {}
    response['images'] = []
    response['images'].append({'location': image_one_path})
    response['images'].append({'location': image_two_path})
    response['outputName'] = image_one_path[:-4] + "_diff.png"

    IMAGE_ONE = Image.open(image_one_path)
    IMAGE_TWO = Image.open(image_two_path)

    response['images'][0]['size'] = IMAGE_ONE.size
    response['images'][1]['size'] = IMAGE_TWO.size

    if IMAGE_ONE.size[0] > IMAGE_TWO.size[0]:
        output_width = IMAGE_ONE.size[0]
    else:
        output_width = IMAGE_TWO.size[0]

    if IMAGE_ONE.size[1] > IMAGE_TWO.size[1]:
        output_height = IMAGE_ONE.size[1]
    else:
        output_height = IMAGE_TWO.size[1]

    response['outputSize'] = (output_width, output_height)

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
    for i in range(output_width-1):
        for j in range(output_height-1):
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

    diff_percent = (float(diff_count)/(output_width * output_height))*100

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
            final_image.save(response['outputName'])
        else:
            final_image = Image.blend(IMAGE_ONE, diff_image, 0.25)
            final_image.save(response['outputName'])

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
