from __future__ import absolute_import
from app.image.v2.lib import generate_difference_report
import falcon


class Routes(object):
    def on_post(self, req, resp):
        if 'images' in req.context['doc']:
            images = req.context['doc']['images']
        else:
            raise falcon.HTTPBadRequest(
                'Missing images array',
                'An array of images must be submitted in the request body.')

        if 'threshold' in req.context['doc']:
            threshold = req.context['doc']['threshold']
        else:
            threshold = 0

        if 'returnOutputImage' in req.context['doc']:
            output = req.context['doc']['returnOutputImage']
        else:
            output = False

        if len(images) != 2:
            raise falcon.HTTPBadRequest(
                'Missing images array',
                'An array of images must contain exactly 2 images.')
        resp.status = falcon.HTTP_OK
        report = generate_difference_report(images[0],
                                            images[1],
                                            create_diff_file=output,
                                            diff_threshold=threshold)

        req.context['result'] = report
