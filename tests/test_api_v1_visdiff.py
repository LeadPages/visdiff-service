import unittest
import os
import base64
import json
from app import create_app
from flask import url_for

FIXTURES_FOLDER = os.path.join(os.path.dirname(__file__), 'fixtures')
IMAGE_ONE = os.path.join(FIXTURES_FOLDER, 'launchpage_after_1024.png')
IMAGE_TWO = os.path.join(FIXTURES_FOLDER, 'launchpage_before_1024.png')


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with open(IMAGE_ONE, 'rb') as f:
            self.launchpage_after_1024_base64 = base64.b64encode(f.read())
        with open(IMAGE_TWO, 'rb') as f:
            self.launchpage_before_1024_base64 = base64.b64encode(f.read())

    def tearDown(self):
        self.app_context.pop()

    def test_launchpad_images(self):
        r = self.client.post(url_for('main.image_diff_endpoint'), data=dict(
            images=[self.launchpage_before_1024_base64,
                    self.launchpage_after_1024_base64]
        ))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'fromString')
        self.assertEqual(data['images'][1]['location'], 'fromString')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [715, 1024])
        self.assertEqual(data['images'][1]['size'], [715, 1024])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [715, 1024])

        self.assertEqual(data['diffCount'], 72766)

        self.assertEqual(data['diffPercent'], 9.938538024475523)
