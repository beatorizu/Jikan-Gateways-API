import requests
from unittest import mock, TestCase
from controller.core import (CharacterNotFoundException, ServiceUnavailable,
                             JikanGatewaysAPI)


class JikanGatewaysAPITest(TestCase):

    def setUp(self):
        # objeto Mock simulando o cliente HTTP
        self.client = mock.Mock(spec=requests)
        self.jikan_data = JikanGatewaysAPI(self.client)

    def test_can_get_ok_response(self):
        self.client.get.return_value = mock.Mock(status_code=200)

        response = self.jikan_data.search_data()

        self.assertEqual(200, response.status_code)

    def test_search_character(self):
        # dicionário com a estrutura básica da resposta da api
        json_response = {
            'result': [
                {'name': 'Suguro, Ryuuji'}
            ]
        }

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        response = self.jikan_data.search_character(name='Ryuuji Suguro')

        content = response.json()

        self.assertEqual('Suguro, Ryuuji', content['result'][0]['name'])

        # verificando a URL da chamada get
        self.client.get.assert_called_with(
            'https://api.jikan.moe/search/character?q=Ryuuji+Suguro'
        )

    def test_not_found_character(self):
        json_response = {
            'error': 'File does not exist'
        }

        mock_response = mock.Mock(status_code=404)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with self.assertRaises(CharacterNotFoundException) as context:
            self.jikan_data.search_character(name='Chapolin')

        self.assertEqual('Character Chapolin not found.',
                         context.exception.message)

    def test_service_unavailable(self):
        json_response = {
            'error': 'Server Error'
        }

        mock_response = mock.Mock(status_code=503)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with self.assertRaises(ServiceUnavailable) as context:
            self.jikan_data.search_character(name='Erza Scarlet')

        self.assertEqual('Service Unavailable.',
                         context.exception.message)
