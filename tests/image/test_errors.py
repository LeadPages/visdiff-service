import unittest
from app import create_app
from flask import url_for
import json


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_404_error(self):
        path = '/bad_path'
        r = self.client.get(path)
        self.assertEqual(r.status_code, 404)
        data = json.loads(r.data)

        self.assertEquals("an error has occured", data["message"])

    def not_test_500_error(self):
        r = self.client.patch(url_for('imagev1.image_diff_endpoint'))
        self.assertEqual(r.status_code, 500)
        data = json.loads(r.data)

        self.assertEquals("an error has occured", data["message"])
