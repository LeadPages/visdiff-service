import falcon
from app.middleware import JSONTranslator
from app.image.v1 import routes as v1
from app.image.v2 import routes as v2

api = application = falcon.API(middleware=[
    JSONTranslator()
])

api.add_route('/images/v1/api/diff', v1.Routes())
api.add_route('/images/v2/api/diff', v2.Routes())
