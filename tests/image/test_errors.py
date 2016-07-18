import unittest
import json
from app.image import errors


class ApiTests(unittest.TestCase):

    def test_404_error(self):
        res = errors.page_not_found("")
        self.assertEqual(res[1], 404)
        data = json.loads(res[0].data)

        self.assertEquals("an error has occured", data["message"])

    def test_500_error(self):
        res = errors.internal_server_error("")
        self.assertEqual(res[1], 500)
        data = json.loads(res[0].data)

        self.assertEquals("an error has occured", data["message"])
