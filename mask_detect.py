import Image
import sys
import math
import subprocess

DIFF_THRESHOLD = 0
IMAGE1 = None


def gen_p_diff():
    """
    Compare the two images passed in to the module from command line
    output to console results and generate a visual diff for humans
    """
    global IMAGE1

    IMAGE1_WIDTH, IMAGE1_HEIGHT = IMAGE1.size

    output_width = IMAGE1_WIDTH

    output_height = IMAGE1_HEIGHT

    PDIFF = "mask_filter.png"

    diff_image = Image.new('RGB', (output_width, output_height))

    image1_pixels = IMAGE1.load()
    diff_pixels = diff_image.load()

    # iterate through the pixels of both images and compare, if different,
    # mark the difference image with yellow so it is noticeable to humans
    #diff_count = 0
    #diff_percent = 0.0
    for i in range(output_width-1):
        for j in range(output_height-1):
            print "dbg: " + str(image1_pixels[i,j])
            if is_masked(image1_pixels[i,j]):
                diff_pixels = image1_pixels[i,j]
            #if pixels_are_different(image1_pixels[i, j], image2_pixels[i, j]):
                # write a yellow pixel to the difference mask and
                # increment difference count
                #diff_pixels[i, j] = (128, 128, 0)
                #diff_count += 1
            else:
                diff_pixels = (0,0,0)
                # write a black pixel to the diffrence mask
                #diff_pixels[i, j] = (0, 0, 0)

    # do not blend if images are found to match because blending
    # can be expensive
    #if diff_count != 0:
        # overlay the two input images, then overlay the yellow/black marked
        # difference image to generate the output image that a human can see
    #    final_image = Image.blend(IMAGE1, IMAGE2, 0.5)
    #final_image = Image.blend(diff_image, final_image, 1.0)
    #final_image.save(PDIFF)

    diff_image.save(PDIFF)

    #    diff_percent = (float(diff_count)/(output_width * output_height))*100

    # it is up to whatever consumes this output to determine whether the
    # calculated diff percentage or count of different
    # pixels is acceptible or not
    #print "Detected %d different pixels, %f percent difference\n" \
    #    % (diff_count, diff_percent)

    subprocess.call(["open", "mask_filter.png"])


def is_masked(pixel):
    #if pixel[0] == 250 and pixel[1] == 1 and pixel[3] == 253:
    if pixel[0] in range(240, 255) and pixel[1] in range(0, 4) and pixel[2] in range(250, 255):
        print "FOUND MASK!"
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
    global DIFF_THRESHOLD
    for component in range(3):
        if math.fabs(pixel1[component] - pixel2[component]) > DIFF_THRESHOLD:
            return True

    return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Please specify both ImageA and ImageB and a difference " \
                " threshold (suggested: 40)\n >python pdiff.py <ImageA> <ImageB> <threshold>\n"
        sys.exit("Wrong number of arguments")

    IMAGE1 = Image.open(sys.argv[1])

    gen_p_diff()
