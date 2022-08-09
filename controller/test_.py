from unittest import mock

import pytest
import requests

from controller.core import (AnimeNotFoundException,
                             CharacterNotFoundException, JikanGatewaysAPI,
                             MangaNotFoundException, PersonNotFoundException,
                             SeasonNotFoundException, ServiceUnavailable)


class TestJikanGatewaysAPI:

    @pytest.fixture(autouse=True)
    def setUp(self):
        # objeto Mock simulando o cliente HTTP
        self.client = mock.Mock(spec=requests)
        self.jikan_data = JikanGatewaysAPI(self.client)

    def test_can_get_ok_response(self):
        self.client.get.return_value = mock.Mock(status_code=200)

        response = self.jikan_data.search_data()

        assert response.status_code == 200

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

        assert content['result'][0]['name'] == 'Suguro, Ryuuji'

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

        with pytest.raises(CharacterNotFoundException) as context:
            self.jikan_data.search_character(name='Chapolin')
        assert context.value.message == 'Character Chapolin not found.'

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

        assert 'Redline' == content['result'][0]['title']

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

        with pytest.raises(AnimeNotFoundException) as context:
            self.jikan_data.search_anime(name='The Smurfs')

        assert context.value.message == 'Anime The Smurfs not found.'

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

        assert content['anime'][0]['title'] == 'Violet Evergarden'

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

        with pytest.raises(SeasonNotFoundException) as context:
            self.jikan_data.list_animes_from_season(year=2018, season=2)

        assert context.value.message == 'Year 2018, Season 2 not found.'

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

        assert content['result'][0]['title'] == 'Shingeki no Kyojin'

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

        with pytest.raises(MangaNotFoundException) as context:
            self.jikan_data.search_manga(name='Avatar: The Last Airbender')

        assert context.value.message == 'Manga Avatar: The Last Airbender not found.'

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

        assert content['result'][0]['name'] == 'Hayami, Show'

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

        with pytest.raises(PersonNotFoundException) as context:
            self.jikan_data.search_person(name='Antonio Vivaldi')

        assert 'Person Antonio Vivaldi not found.' == context.value.message

    def test_service_unavailable(self):
        json_response = {
            'error': 'Server Error'
        }

        mock_response = mock.Mock(status_code=503)
        mock_response.json.return_value = json_response
        self.client.get.return_value = mock_response

        with pytest.raises(ServiceUnavailable) as context:
            self.jikan_data.search_character(name='Erza Scarlet')

        assert context.value.message == 'Service Unavailable.'
