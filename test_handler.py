import json
import unittest
import handler

class calculationTest(unittest.TestCase):

    def setUp(self):
        self.event = {}
        result = handler.get(self.event,'')
        data = json.loads(result["body"])

        self.views = data["views"]

    def test_handler_get(self):
        self.assertIsInstance(self.views, int)

    def test_handler_update(self):
        mock_additional_view = handler.update(self.event, '')

        get_additional_view = handler.get(self.event,'')
        data = json.loads(get_additional_view["body"])
        additional_view = data["views"]

        self.assertEqual(self.views + 2, additional_view)