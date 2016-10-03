from __future__ import absolute_import
from app.image.v1.lib import generate_difference_report
import falcon


class Routes(object):
    def on_post(self, req, resp):
        if 'images' in req.context['doc']:
            images = req.context['doc']['images']
        else:
            raise falcon.HTTPBadRequest(
                'Missing images array',
                'An array of images must be submitted in the request body.')
        if len(images) != 2:
            raise falcon.HTTPBadRequest(
                'Missing images array',
                'An array of images must contain exactly 2 images.')
        resp.status = falcon.HTTP_OK
        req.context['result'] = generate_difference_report(images[0],
                                                           images[1])
