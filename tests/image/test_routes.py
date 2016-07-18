import unittest
from app import create_app
from flask import url_for
from fixtures import test_images


class TestPageRouteTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_GET_image_diff_test_page(self):
        r = self.client.get(url_for('image.image_diff_test_page'))
        self.assertEqual(r.status_code, 200)

    def test_POST_v1_image_diff_test_page(self):
        with self.app.open_resource(test_images.LAUNCHPAGE_AFTER) as one:
            with self.app.open_resource(test_images.LAUNCHPAGE_BEFORE) as two:
                r = self.client.post(
                    url_for('image.image_diff_test_page'),
                    data={
                        'image_one': one,
                        'image_two': two,
                        'version_radio_button': "v1"}
                )
                self.assertEqual(r.status_code, 200)
                self.assertIn('v1', r.data,
                              'Api version not found in the resulting page')
                self.assertIn('Image Difference Report', r.data,
                              'Api version not found in the resulting page')

    def test_POST_v2_image_diff_test_page(self):
        with self.app.open_resource(test_images.LAUNCHPAGE_AFTER) as one:
            with self.app.open_resource(test_images.LAUNCHPAGE_BEFORE) as two:
                r = self.client.post(
                    url_for('image.image_diff_test_page'),
                    data={
                        'image_one': one,
                        'image_two': two,
                        'version_radio_button': "v2"}
                )
                self.assertEqual(r.status_code, 200)
                self.assertIn('v2', r.data,
                              'Api version not found in the resulting page')
                self.assertIn('Image Difference Report', r.data,
                              'Header Found')

    def test_POST_image_diff_test_page_invalid_form(self):
        with self.app.open_resource(test_images.LAUNCHPAGE_BEFORE) as two:
            r = self.client.post(
                url_for('image.image_diff_test_page'),
                data={
                    'image_two': two,
                    'version_radio_button': "v1"}
            )
            self.assertEqual(r.status_code, 200)
            self.assertIn('Please enter two images to compare', r.data)
