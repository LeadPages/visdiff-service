import unittest
import base64
import json
from app import create_app
from flask import url_for
import time
from fixtures import test_images

# Limit for how long all api requests should be under
API_REQUEST_TIMEOUT = 3


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_launchpad_images(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [715, 1024])
        self.assertEqual(data['images'][1]['size'], [715, 1024])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [715, 1024])

        self.assertEqual(data['diffCount'], 167333)

        self.assertEqual(data['diffPercent'], 22.85470388986014)

    def test_spot_images(self):
        """Compares the spot images.  Both are 3MB plus"""
        with open(test_images.SPOT_THREE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SPOT_FOUR, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [1600, 1200])
        self.assertEqual(data['images'][1]['size'], [1600, 1200])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [1600, 1200])

        self.assertEqual(data['diffCount'], 65492)

        self.assertEqual(data['diffPercent'],  3.4110416666666663)

    def test_more_spot_images(self):
        with open(test_images.SPOT_ONE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SPOT_TWO, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [347, 383])
        self.assertEqual(data['images'][1]['size'], [347, 383])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [347, 383])

        self.assertEqual(data['diffCount'], 6683)

        self.assertEqual(data['diffPercent'], 5.028555089878933)

    def test_hard_spot_images(self):
        with open(test_images.SPOT_HARD_ONE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SPOT_HARD_TWO, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [245, 361])
        self.assertEqual(data['images'][1]['size'], [245, 361])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [245, 361])

        self.assertEqual(data['diffCount'], 88198)

        self.assertEqual(data['diffPercent'], 99.72073039742213)

    def test_leadbox_images(self):
        with open(test_images.LEADBOX_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.LEADBOX_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 1436])
        self.assertEqual(data['images'][1]['size'], [2868, 1436])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 1436])

        self.assertEqual(data['diffCount'], 537404)

        self.assertEqual(data['diffPercent'], 13.048701841081883)

    def test_thank_you_images(self):
        with open(test_images.THANKS_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.THANKS_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 2446])
        self.assertEqual(data['images'][1]['size'], [2868, 2446])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 2446])

        self.assertEqual(data['diffCount'], 490706)

        self.assertEqual(data['diffPercent'], 6.994968587886066)

    def test_share_page_images(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_two]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 2826])
        self.assertEqual(data['images'][1]['size'], [2868, 2826])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 2826])

        self.assertEqual(data['diffCount'], 2398926)

        self.assertEqual(data['diffPercent'], 29.5982167974013)

    def test_same_images(self):
        with open(test_images.SPOT_THREE, 'rb') as f:
            image_one = base64.b64encode(f.read())

        start = time.time()
        r = self.client.post(url_for('image.image_diff_endpoint_v2'),
                             data=dict(
                                    images=[image_one, image_one]
                                    ))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = json.loads(r.data)

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [1600, 1200])
        self.assertEqual(data['images'][1]['size'], [1600, 1200])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [1600, 1200])

        self.assertEqual(data['diffCount'], 0)

        self.assertEqual(data['diffPercent'], 0)
