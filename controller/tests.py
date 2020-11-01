import requests
from unittest import mock, TestCase
from controller.core import (CharacterNotFoundException,
                             AnimeNotFoundException,
                             SeasonNotFoundException,
                             MangaNotFoundException,
                             PersonNotFoundException,
                             ServiceUnavailable,
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
        print(response.text)

        content = response.json()

        self.assertEqual('Suguro, Ryuuji', content['result'][0]['name'])

        # verificando a URL da chamada get
        self.client.get.assert_called_with(
            'https://api.jikan.moe/v3/search/character?q=Ryuuji+Suguro'
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

    def test_search_anime(self):
        # dicionário com a estrutura básica da resposta da api
        json_response = {
            'result': [
                {'title': 'Redline'}
            ]
        }

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        response = self.jikan_data.search_anime(name='Redline')
        print(response.text)

        content = response.json()

        self.assertEqual('Redline', content['result'][0]['title'])

        # verificando a URL da chamada get
        self.client.get.assert_called_with(
            'https://api.jikan.moe/v3/search/anime?q=Redline'
        )

    def test_not_found_anime(self):
        json_response = {
            'error': 'File does not exist'
        }

        mock_response = mock.Mock(status_code=404)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with self.assertRaises(AnimeNotFoundException) as context:
            self.jikan_data.search_anime(name='The Smurfs')

        self.assertEqual('Anime The Smurfs not found.',
                         context.exception.message)

    def test_list_anime_of_season(self):
        # dicionário com a estrutura básica da resposta da api
        json_response = {
            'anime': [
                {
                    'title': 'Violet Evergarden',
                    'episodes': 13
                }
            ]
        }

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        response = self.jikan_data.list_animes_from_season(year=2018, season='winter')
        print(response.text)

        content = response.json()

        self.assertEqual('Violet Evergarden', content['anime'][0]['title'])

        # verificando a URL da chamada get
        self.client.get.assert_called_with(
            'https://api.jikan.moe/v3/season/2018/winter'
        )

    def test_not_found_anime_of_season(self):
        json_response = {
            'error': 'File does not exist'
        }

        mock_response = mock.Mock(status_code=404)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with self.assertRaises(SeasonNotFoundException) as context:
            self.jikan_data.list_animes_from_season(year=2018, season=2)

        self.assertEqual('Year 2018, Season 2 not found.',
                         context.exception.message)

    def test_search_manga(self):
        # dicionário com a estrutura básica da resposta da api
        json_response = {
            'result': [
                {'title': 'Shingeki no Kyojin'}
            ]
        }

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        response = self.jikan_data.search_manga(name='Shingeki no Kyojin')
        print(response.text)

        content = response.json()

        self.assertEqual('Shingeki no Kyojin', content['result'][0]['title'])

        # verificando a URL da chamada get
        self.client.get.assert_called_with(
            'https://api.jikan.moe/v3/search/manga?q=Shingeki+no+Kyojin'
        )

    def test_not_found_manga(self):
        json_response = {
            'error': 'File does not exist'
        }

        mock_response = mock.Mock(status_code=404)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with self.assertRaises(MangaNotFoundException) as context:
            self.jikan_data.search_manga(name='Avatar: The Last Airbender')

        self.assertEqual('Manga Avatar: The Last Airbender not found.',
                         context.exception.message)

    def test_search_person(self):
        # dicionário com a estrutura básica da resposta da api
        json_response = {
            'result': [
                {'name': 'Hayami, Show'}
            ]
        }

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        response = self.jikan_data.search_person(name='Hayami')
        print(response.text)

        content = response.json()

        self.assertEqual('Hayami, Show', content['result'][0]['name'])

        # verificando a URL da chamada get
        self.client.get.assert_called_with(
            'https://api.jikan.moe/v3/search/people?q=Hayami'
        )

    def test_not_found_person(self):
        json_response = {
            'error': 'File does not exist'
        }

        mock_response = mock.Mock(status_code=404)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with self.assertRaises(PersonNotFoundException) as context:
            self.jikan_data.search_person(name='Antonio Vivaldi')

        self.assertEqual('Person Antonio Vivaldi not found.',
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
