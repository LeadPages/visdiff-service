import unittest
from app import image_diff
from fixtures import test_images
import os
import base64


class GenerateDifferenceReportWithFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.res = image_diff.\
            generate_difference_report(test_images.LAUNCHPAGE_AFTER,
                                       test_images.LAUNCHPAGE_BEFORE)

    def test_location_added(self):
        self.assertEqual(self.res['images'][0]['location'],
                         test_images.LAUNCHPAGE_AFTER)
        self.assertEqual(self.res['images'][1]['location'],
                         test_images.LAUNCHPAGE_BEFORE)

    def test_size_added(self):
        self.assertEqual(self.res['images'][0]['size'], (715, 1024))
        self.assertEqual(self.res['images'][1]['size'], (715, 1024))

    def test_mode_added(self):
        self.assertEqual(self.res['images'][0]['mode'], 'RGBA')
        self.assertEqual(self.res['images'][1]['mode'], 'RGBA')

    def test_diff_count(self):
        self.assertEqual(self.res['diffCount'], 72766)

    def test_output_size(self):
        self.assertEqual(self.res['outputSize'], (715, 1024))

    def test_diff_percent(self):
        self.assertEqual(self.res['diffPercent'], 9.938538024475523)


class GenerateDifferenceReportWithBase64StringTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, 'rb') as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())
        self.res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)

    def test_location_added(self):
        self.assertEqual(self.res['images'][0]['location'], 'fromString')
        self.assertEqual(self.res['images'][1]['location'], 'fromString')

    def test_size_added(self):
        self.assertEqual(self.res['images'][0]['size'], (715, 1024))
        self.assertEqual(self.res['images'][1]['size'], (715, 1024))

    def test_mode_added(self):
        self.assertEqual(self.res['images'][0]['mode'], 'RGBA')
        self.assertEqual(self.res['images'][1]['mode'], 'RGBA')

    def test_diff_count(self):
        self.assertEqual(self.res['diffCount'], 72766)

    def test_output_size(self):
        self.assertEqual(self.res['outputSize'], (715, 1024))

    def test_diff_percent(self):
        self.assertEqual(self.res['diffPercent'], 9.938538024475523)


class LoadImageTests(unittest.TestCase):
    def test_load_image_from_file(self):
        img = image_diff.load_image(test_images.LAUNCHPAGE_AFTER)
        self.assertEquals(img.size, (715, 1024))

    def test_load_image_from_string(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            img = image_diff.load_image(base64.b64encode(f.read()))
            self.assertEquals(img.size, (715, 1024))

    def test_load_large_image_from_file(self):
        img = image_diff.load_image(test_images.SPOT_THREE)
        self.assertEquals(img.size, (1600, 1200))

    def test_load_large_image_from_string(self):
        with open(test_images.SPOT_THREE, 'rb') as f:
            img = image_diff.load_image(base64.b64encode(f.read()))
            self.assertEquals(img.size, (1600, 1200))

    def test_load_image_empty_string(self):
        with self.assertRaises(IOError):
            image_diff.load_image('')

    def test_load_image_from_file_that_does_not_exist(self):
        fake_file = os.path.join(os.path.dirname(__file__), 'fake_file.png')
        with self.assertRaises(IOError):
            image_diff.load_image(fake_file)
