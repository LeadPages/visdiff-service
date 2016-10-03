from __future__ import absolute_import
import unittest
from app.image.image_lib import load_image, get_output_image_size
from tests.fixtures import test_images
import os
import base64
from PIL import Image


class LoadImageTests(unittest.TestCase):
    def setUp(self):
        self.file_error_message = "Image type was not listed in supported" +\
                                  " images \('jpg', 'jpe', 'jpeg', 'png'," +\
                                  " 'bmp'\)"

    def test_jpg_load(self):
        img = load_image(test_images.PK_1000_x_1000_JPG)
        self.assertEquals(img.size, (1000, 1000))

    def test_jpe_load(self):
        img = load_image(test_images.PK_1000_x_1000_JPE)
        self.assertEquals(img.size, (1000, 1000))

    def test_jpeg_load(self):
        img = load_image(test_images.PK_200_x_300)
        self.assertEquals(img.size, (200, 300))

    def test_png_load(self):
        img = load_image(test_images.LEADBOX_BEFORE)
        self.assertEquals(img.size, (2868, 1436))

    def test_svg_load(self):
        with self.assertRaisesRegexp(ValueError, self.file_error_message):
            load_image(test_images.KIWI_400_x_400_SVG)

    def test_bmp_load(self):
        img = load_image(test_images.MOUNTAIN_640_x_480_BMP)
        self.assertEquals(img.size, (640, 480))

    def test_unsupported_image(self):
        with self.assertRaisesRegexp(ValueError, self.file_error_message):
            load_image(test_images.NOT_IMAGE)

    def test_load_image_from_file(self):
        img = load_image(test_images.LAUNCHPAGE_AFTER)
        self.assertEquals(img.size, (715, 1024))

    def test_load_image_from_string(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            img = load_image(base64.b64encode(f.read()))
            self.assertEquals(img.size, (715, 1024))

    def test_load_large_image_from_file(self):
        img = load_image(test_images.SPOT_THREE)
        self.assertEquals(img.size, (1600, 1200))

    def test_load_large_image_from_string(self):
        with open(test_images.SPOT_THREE, 'rb') as f:
            img = load_image(base64.b64encode(f.read()))
            self.assertEquals(img.size, (1600, 1200))

    def test_load_image_empty_string(self):
        with self.assertRaises(IOError):
            load_image('')

    def test_load_image_from_file_that_does_not_exist(self):
        fake_file = os.path.join(os.path.dirname(__file__), 'fake_file.png')
        with self.assertRaises(IOError):
            load_image(fake_file)


class ImageGetOutputSizeTests(unittest.TestCase):
    def test_string_input_throws_error(self):
        """Function should throw an error is a string is given"""
        with self.assertRaisesRegexp(ValueError,
                                     "Both parameters must be of type Image"):
            get_output_image_size("one", "two")

    def test_one_is_image_and_two_is_tuple(self):
        """Function should throw an error is a string is given"""
        img_one = Image.open(test_images.LAUNCHPAGE_AFTER)
        with self.assertRaisesRegexp(ValueError,
                                     "Both parameters must be of type Image"):
            get_output_image_size(img_one, (1, 3, 4))

    def test_two_is_image_and_one_is_array(self):
        """Function should throw an error is a string is given"""
        img_two = Image.open(test_images.LAUNCHPAGE_AFTER)
        with self.assertRaisesRegexp(ValueError,
                                     "Both parameters must be of type Image"):
            get_output_image_size([1, 3, 5], img_two)

    def test_same_image(self):
        """Image one and Image two are identical"""
        img_one = Image.open(test_images.LAUNCHPAGE_AFTER)
        img_two = Image.open(test_images.LAUNCHPAGE_AFTER)

        size = get_output_image_size(img_one, img_two)

        self.assertEqual(size, (715, 1024))

    def test_image_one_larger_than_image_two(self):
        """Image one is larger than image two"""
        img_one = Image.open(test_images.SPOT_THREE)
        img_two = Image.open(test_images.LAUNCHPAGE_AFTER)

        size = get_output_image_size(img_one, img_two)

        self.assertEqual(size, (1600, 1200))

    def test_image_two_larger_than_image_one(self):
        """Image two is larger than image one"""
        img_one = Image.open(test_images.LAUNCHPAGE_AFTER)
        img_two = Image.open(test_images.SPOT_FOUR)

        size = get_output_image_size(img_one, img_two)

        self.assertEqual(size, (1600, 1200))

    def test_size_mixed_for_images(self):
        """Image one is wider and image two is taller"""
        img_one = Image.open(test_images.PK_300_x_200)
        img_two = Image.open(test_images.PK_200_x_300)

        size = get_output_image_size(img_one, img_two)

        self.assertEqual(size, (300, 300))
