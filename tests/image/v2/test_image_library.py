import unittest
from app.image.v2.lib import generate_difference_report, get_boolean
from tests.fixtures import test_images
import base64


class GenerateDifferenceReportWithFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.res = generate_difference_report(test_images.LAUNCHPAGE_AFTER,
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
        self.assertEqual(self.res['diffCount'], 167333)

    def test_output_size(self):
        self.assertEqual(self.res['outputSize'], (715, 1024))

    def test_diff_percent(self):
        self.assertEqual(self.res['diffPercent'], 22.85470388986014)


class GenerateDifferenceReportWithBase64StringTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, 'rb') as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())
        self.res = generate_difference_report(
                    self.launchpage_after_1024_base64,
                    self.launchpage_before_1024_base64)

    def test_location_added(self):
        self.assertEqual(self.res['images'][0]['location'], 'base64string')
        self.assertEqual(self.res['images'][1]['location'], 'base64string')

    def test_size_added(self):
        self.assertEqual(self.res['images'][0]['size'], (715, 1024))
        self.assertEqual(self.res['images'][1]['size'], (715, 1024))

    def test_mode_added(self):
        self.assertEqual(self.res['images'][0]['mode'], 'RGBA')
        self.assertEqual(self.res['images'][1]['mode'], 'RGBA')

    def test_diff_count(self):
        self.assertEqual(self.res['diffCount'], 167333)

    def test_output_size(self):
        self.assertEqual(self.res['outputSize'], (715, 1024))

    def test_diff_percent(self):
        self.assertEqual(self.res['diffPercent'], 22.85470388986014)


class GenerateDifferenceReportWithOutputTests(unittest.TestCase):
    def setUp(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, 'rb') as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())

    def test_output_created(self):
        res = generate_difference_report(
                    self.launchpage_after_1024_base64,
                    self.launchpage_before_1024_base64,
                    True)
        self.assertIsNotNone(res["outputImage"])

    def test_output_empty(self):
        res = generate_difference_report(
                    self.launchpage_after_1024_base64,
                    self.launchpage_before_1024_base64)
        self.assertIsNone(res["outputImage"])

    def test_no_diff_count(self):
        res = generate_difference_report(
                    self.launchpage_after_1024_base64,
                    self.launchpage_after_1024_base64,
                    True)
        self.assertIsNotNone(res["outputImage"])


class GetBooleanTests(unittest.TestCase):
    def test_true_string_cases(self):
        self.assertTrue(get_boolean('true'))
        self.assertTrue(get_boolean('yes'))
        self.assertTrue(get_boolean('on'))
        self.assertTrue(get_boolean('y'))
        self.assertTrue(get_boolean('1'))

    def test_false_string_cases(self):
        self.assertFalse(get_boolean('false'))
        self.assertFalse(get_boolean('no'))
        self.assertFalse(get_boolean('off'))
        self.assertFalse(get_boolean('n'))
        self.assertFalse(get_boolean('0'))

    def test_true_bool_cases(self):
        self.assertTrue(get_boolean(True))

    def test_false_bool_cases(self):
        self.assertFalse(get_boolean(False))

    def test_null_cases(self):
        with self.assertRaises(ValueError):
            get_boolean(None)

    def test_unhandled_cases(self):
        with self.assertRaises(ValueError):
            get_boolean('neither')
