from __future__ import absolute_import
import unittest
from app.image.v1.lib import generate_difference_report
from tests.fixtures import test_images
import base64


class GenerateDifferenceReportWithFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.res = generate_difference_report(test_images.LAUNCHPAGE_AFTER,
                                              test_images.LAUNCHPAGE_BEFORE)

    def test_location_added(self):
        self.assertEqual(self.res["images"][0]["location"],
                         test_images.LAUNCHPAGE_AFTER)
        self.assertEqual(self.res["images"][1]["location"],
                         test_images.LAUNCHPAGE_BEFORE)

    def test_size_added(self):
        self.assertEqual(self.res["images"][0]["size"], (715, 1024))
        self.assertEqual(self.res["images"][1]["size"], (715, 1024))

    def test_mode_added(self):
        self.assertEqual(self.res["images"][0]["mode"], "RGBA")
        self.assertEqual(self.res["images"][1]["mode"], "RGBA")

    def test_diff_count(self):
        self.assertEqual(self.res["diffCount"], 72766)

    def test_output_size(self):
        self.assertEqual(self.res["outputSize"], (715, 1024))

    def test_diff_percent(self):
        self.assertEqual(self.res["diffPercent"], 9.938538024475523)


class GenerateDifferenceReportWithBase64StringTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open(test_images.LAUNCHPAGE_AFTER, "rb") as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, "rb") as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())
        self.res = generate_difference_report(
                    self.launchpage_after_1024_base64,
                    self.launchpage_before_1024_base64)

    def test_location_added(self):
        self.assertEqual(self.res["images"][0]["location"], "base64string")
        self.assertEqual(self.res["images"][1]["location"], "base64string")

    def test_size_added(self):
        self.assertEqual(self.res["images"][0]["size"], (715, 1024))
        self.assertEqual(self.res["images"][1]["size"], (715, 1024))

    def test_mode_added(self):
        self.assertEqual(self.res["images"][0]["mode"], "RGBA")
        self.assertEqual(self.res["images"][1]["mode"], "RGBA")

    def test_diff_count(self):
        self.assertEqual(self.res["diffCount"], 72766)

    def test_output_size(self):
        self.assertEqual(self.res["outputSize"], (715, 1024))

    def test_diff_percent(self):
        self.assertEqual(self.res["diffPercent"], 9.938538024475523)


class GenerateDifferenceReportWithOutputTests(unittest.TestCase):
    def setUp(self):
        with open(test_images.LAUNCHPAGE_AFTER, "rb") as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, "rb") as f:
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


class ReportWithMaskTests(unittest.TestCase):
    def setUp(self):
        with open(test_images.LAUNCHPAGE_MASKED_ONE, "rb") as f:
            self.launchpage_masked_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_AFTER, "rb") as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, "rb") as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())

    def test_output_created(self):
        res_masked = generate_difference_report(
                    self.launchpage_masked_1024_base64,
                    self.launchpage_after_1024_base64,
                    False)
        res = generate_difference_report(
                    self.launchpage_before_1024_base64,
                    self.launchpage_after_1024_base64,
                    False)
        self.assertGreater(res["diffCount"], res_masked["diffCount"])
