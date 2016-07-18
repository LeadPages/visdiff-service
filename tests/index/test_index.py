import unittest
from app import create_app
from flask import url_for


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_index_redirect(self):
        r = self.client.get(url_for('index.index_page'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.location,
                         url_for('image.image_diff_test_page', _external=True))
