import unittest
from app.image.image_lib import load_image
from fixtures import test_images
import os
import base64


class LoadImageTests(unittest.TestCase):
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
