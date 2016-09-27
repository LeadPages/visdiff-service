import base64
import json
import time
from tests.fixtures import test_images
import falcon.testing as testing
from app.image.v2 import routes as v2
import falcon
from app.middleware import JSONTranslator

# Limit for how long all api requests should be under
API_REQUEST_TIMEOUT = 5


class ApiTests(testing.TestCase):
    def setUp(self):
        super(ApiTests, self).setUp()
        self.api = falcon.API(middleware=[
            JSONTranslator()
        ])
        route = v2.Routes()
        self.api.add_route('/images/v2/api/diff', route)

    def test_launchpad_images(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))

        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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

        self.assertIsNone(data['outputImage'])

    def test_share_page_images_with_return_on(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'returnOutputImage': True}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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

        self.assertIsNotNone(data['outputImage'])

    def test_same_images(self):
        with open(test_images.SPOT_THREE, 'rb') as f:
            image_one = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_one]}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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

    def test_one_image_error(self):
        with open(test_images.SPOT_THREE, 'rb') as f:
            image_one = base64.b64encode(f.read())

        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one]}))
        self.assertEqual(r.status_code, 400)

        data = r.json
        self.assertEqual(data["description"],
                         "An array of images must contain exactly 2 images.")
        self.assertEqual(data["title"],
                         "Missing images array")


class ApiWithThresholdTests(testing.TestCase):
    def setUp(self):
        super(ApiWithThresholdTests, self).setUp()
        self.api = falcon.API(middleware=[
            JSONTranslator()
        ])
        route = v2.Routes()
        self.api.add_route('/images/v2/api/diff', route)

    def test_launchpad_images(self):
        with open(test_images.LAUNCHPAGE_AFTER, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.LAUNCHPAGE_BEFORE, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [715, 1024])
        self.assertEqual(data['images'][1]['size'], [715, 1024])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [715, 1024])

        self.assertEqual(data['diffCount'], 72766)

        self.assertEqual(data['diffPercent'], 9.938538024475523)

    def test_spot_images(self):
        """Compares the spot images.  Both are 3MB plus"""
        with open(test_images.SPOT_THREE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SPOT_FOUR, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [1600, 1200])
        self.assertEqual(data['images'][1]['size'], [1600, 1200])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [1600, 1200])

        self.assertEqual(data['diffCount'], 15278)

        self.assertEqual(data['diffPercent'], 0.7957291666666666)

    def test_more_spot_images(self):
        with open(test_images.SPOT_ONE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SPOT_TWO, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [347, 383])
        self.assertEqual(data['images'][1]['size'], [347, 383])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [347, 383])

        self.assertEqual(data['diffCount'], 5564)

        self.assertEqual(data['diffPercent'], 4.1865749693380785)

        self.assertIsNone(data['outputImage'])

    def test_hard_spot_images(self):
        with open(test_images.SPOT_HARD_ONE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SPOT_HARD_TWO, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [245, 361])
        self.assertEqual(data['images'][1]['size'], [245, 361])

        self.assertEqual(data['images'][0]['mode'], 'RGB')
        self.assertEqual(data['images'][1]['mode'], 'RGB')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [245, 361])

        self.assertEqual(data['diffCount'], 7923)

        self.assertEqual(data['diffPercent'], 8.958109559613318)

        self.assertEqual(data['threshold'], 40)

    def test_leadbox_images(self):
        with open(test_images.LEADBOX_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.LEADBOX_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 1436])
        self.assertEqual(data['images'][1]['size'], [2868, 1436])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 1436])

        self.assertEqual(data['diffCount'], 460277)

        self.assertEqual(data['diffPercent'], 11.175981826163643)

    def test_thank_you_images(self):
        with open(test_images.THANKS_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.THANKS_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 2446])
        self.assertEqual(data['images'][1]['size'], [2868, 2446])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 2446])

        self.assertEqual(data['diffCount'], 482970)

        self.assertEqual(data['diffPercent'], 6.8846926242828355)

    def test_share_page_images(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 2826])
        self.assertEqual(data['images'][1]['size'], [2868, 2826])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 2826])

        self.assertEqual(data['diffCount'], 247907)

        self.assertEqual(data['diffPercent'], 3.058704241645371)

    def test_same_images(self):
        with open(test_images.SPOT_THREE, 'rb') as f:
            image_one = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_one],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

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

    def test_share_page_images_with_return_on(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40,
                                                'returnOutputImage': True}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['images'][0]['location'], 'base64string')
        self.assertEqual(data['images'][1]['location'], 'base64string')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['images'][0]['size'], [2868, 2826])
        self.assertEqual(data['images'][1]['size'], [2868, 2826])

        self.assertEqual(data['images'][0]['mode'], 'RGBA')
        self.assertEqual(data['images'][1]['mode'], 'RGBA')

        # Size will come back as array instead of tuple due to json transform
        self.assertEqual(data['outputSize'], [2868, 2826])

        self.assertEqual(data['diffCount'], 247907)

        self.assertEqual(data['diffPercent'], 3.058704241645371)

        self.assertIsNotNone(data['outputImage'])

    def test_default_result_output_is_false(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'threshold': 40}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertIsNone(data['outputImage'])

    def test_default_threshold_is_zero(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'returnOutputImage': True}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['threshold'], 0)
        self.assertIsNotNone(data['outputImage'])

    def test_false_result_image(self):
        with open(test_images.SHAREPAGE_BEFORE, 'rb') as f:
            image_one = base64.b64encode(f.read())
        with open(test_images.SHAREPAGE_AFTER, 'rb') as f:
            image_two = base64.b64encode(f.read())

        start = time.time()
        r = self.simulate_post('/images/v2/api/diff',
                               body=json.dumps({'images':
                                               [image_one, image_two],
                                               'returnOutputImage': False}))
        end = time.time()
        elapsedTime = end - start
        self.assertLess(elapsedTime, API_REQUEST_TIMEOUT,
                        'request took %s, which is longer than %s seconds'
                        % (elapsedTime, API_REQUEST_TIMEOUT))
        self.assertEqual(r.status_code, 200)

        data = r.json

        self.assertEqual(data['threshold'], 0)
        self.assertIsNone(data['outputImage'])
