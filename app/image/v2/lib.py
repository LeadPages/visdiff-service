from PIL import Image, ImageColor
import numpy as np
from ..image_lib import is_file, load_image, get_output_image_size,\
                        image_blender, get_diff_percent


def generate_difference_report(image_one, image_two,
                               create_diff_file=False,
                               diff_mask_color="yellow"):
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

    # Subtract array representations of both images (matching pixels are
    # returned as (0,0,0) or (0,0,0,0))
    diff_arr = np.subtract(np.asarray(IMAGE_ONE, dtype=np.uint8()),
                           np.asarray(IMAGE_TWO, dtype=np.uint8()))

    # Compare axis 2 (RGB or RGBA values) to black (matching pixels).  If the
    # pixel is anything but black (meaning no match) the comparison will return
    # true.  Sum of true values equals the number of pixels that do not match
    # between the images
    match_arr = ImageColor.getcolor('black', IMAGE_ONE.mode)
    # Color returns rgba value of (0,0,0,255) which throws off matching
    if IMAGE_ONE.mode == "RGBA":
        match_arr = match_arr[:3] + (0,)
    diff_mask = np.any(diff_arr != match_arr, axis=2)
    response['diffCount'] = np.sum(diff_mask)
    response['diffPercent'] = get_diff_percent(response['diffCount'],
                                               response["outputSize"])

    if create_diff_file:
        diff_image = Image.fromarray(diff_arr, IMAGE_ONE.mode)
        mask_color = ImageColor.getcolor(diff_mask_color, IMAGE_ONE.mode)
        diff_arr[diff_mask] = np.array(mask_color)
        diff_image = Image.fromarray(diff_arr, IMAGE_ONE.mode)
        response['outputImage'] = image_blender(IMAGE_ONE,
                                                IMAGE_TWO,
                                                diff_image,
                                                response['diffCount'])
    else:
        response["outputImage"] = None

    return response
