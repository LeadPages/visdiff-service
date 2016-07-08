import unittest
from app import image_diff
import os
import base64

FIXTURES_FOLDER = os.path.join(os.path.dirname(__file__), 'fixtures')
IMAGE_ONE = os.path.join(FIXTURES_FOLDER, 'launchpage_after_1024.png')
IMAGE_TWO = os.path.join(FIXTURES_FOLDER, 'launchpage_before_1024.png')
DIFF_FILE = os.path.join(FIXTURES_FOLDER, 'launchpage_before_1024_diff.png')
LARGE_IMAGE = os.path.join(FIXTURES_FOLDER, 'spot3.png')


class GenerateDifferenceReportWithFileTests(unittest.TestCase):

    def test_location_added(self):
        res = image_diff.generate_difference_report(IMAGE_ONE, IMAGE_TWO)
        self.assertEqual(res['images'][0]['location'], IMAGE_ONE)
        self.assertEqual(res['images'][1]['location'], IMAGE_TWO)

    def test_size_added(self):
        res = image_diff.generate_difference_report(IMAGE_ONE, IMAGE_TWO)
        self.assertEqual(res['images'][0]['size'], (715, 1024))
        self.assertEqual(res['images'][1]['size'], (715, 1024))

    def test_mode_added(self):
        res = image_diff.generate_difference_report(IMAGE_ONE, IMAGE_TWO)
        self.assertEqual(res['images'][0]['mode'], 'RGBA')
        self.assertEqual(res['images'][1]['mode'], 'RGBA')

    def test_diff_count(self):
        res = image_diff.generate_difference_report(IMAGE_ONE, IMAGE_TWO)
        self.assertEqual(res['diffCount'], 72766)

    def test_output_size(self):
        res = image_diff.generate_difference_report(IMAGE_ONE, IMAGE_TWO)
        self.assertEqual(res['outputSize'], (715, 1024))

    def test_diff_percent(self):
        res = image_diff.generate_difference_report(IMAGE_ONE, IMAGE_TWO)
        self.assertEqual(res['diffPercent'], 9.938538024475523)


class GenerateDifferenceReportWithBase64StringTests(unittest.TestCase):
    def setUp(self):
        with open(IMAGE_ONE, 'rb') as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(IMAGE_TWO, 'rb') as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())

    def test_location_added(self):
        res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)
        self.assertEqual(res['images'][0]['location'], 'fromString')
        self.assertEqual(res['images'][1]['location'], 'fromString')

    def test_size_added(self):
        res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)
        self.assertEqual(res['images'][0]['size'], (715, 1024))
        self.assertEqual(res['images'][1]['size'], (715, 1024))

    def test_mode_added(self):
        res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)
        self.assertEqual(res['images'][0]['mode'], 'RGBA')
        self.assertEqual(res['images'][1]['mode'], 'RGBA')

    def test_diff_count(self):
        res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)
        self.assertEqual(res['diffCount'], 72766)

    def test_output_size(self):
        res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)
        self.assertEqual(res['outputSize'], (715, 1024))

    def test_diff_percent(self):
        res = image_diff.\
            generate_difference_report(
                self.launchpage_after_1024_base64,
                self.launchpage_before_1024_base64)
        self.assertEqual(res['diffPercent'], 9.938538024475523)


class LoadImageTests(unittest.TestCase):
    def test_load_image_from_file(self):
        img = image_diff.load_image(IMAGE_ONE)
        self.assertEquals(img.size, (715, 1024))

    def test_load_image_from_string(self):
        with open(IMAGE_ONE, 'rb') as f:
            img = image_diff.load_image(base64.b64encode(f.read()))
            self.assertEquals(img.size, (715, 1024))

    def test_load_large_image_from_file(self):
        img = image_diff.load_image(LARGE_IMAGE)
        self.assertEquals(img.size, (1600, 1200))

    def test_load_large_image_from_string(self):
        with open(LARGE_IMAGE, 'rb') as f:
            img = image_diff.load_image(base64.b64encode(f.read()))
            self.assertEquals(img.size, (1600, 1200))

    def test_load_image_empty_string(self):
        with self.assertRaises(IOError):
            image_diff.load_image('')

    def test_load_image_from_file_that_does_not_exist(self):
        fake_file = os.path.join(FIXTURES_FOLDER, 'fake_file.png')
        with self.assertRaises(IOError):
            image_diff.load_image(fake_file)
