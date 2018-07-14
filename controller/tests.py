from unittest import TestCase
from controller.core import JikanGatewaysAPI


class JikanGatewaysAPITest(TestCase):

    def setUp(self):
        self.jikan_data = JikanGatewaysAPI()

    def test_can_get_ok_response(self):
        response = self.jikan_data.search_data()

        self.assertEqual(200, response.status_code)
