from urllib.parse import urlencode
from controller.exceptions import (CharacterNotFoundException,
                                   ServiceUnavailable)


class JikanGatewaysAPI(object):

    URL = 'https://api.jikan.moe/'

    def __init__(self, client_http):
        self.client = client_http

    def search_data(self):
        return self.client.get(self.URL)

    def search_character(self, name):
        resource = 'v3/search/character?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)


        # Not Found
        if response.status_code == 404:
            raise CharacterNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response

    def search_anime(self, name):
        resource = 'v3/search/anime?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)


        # Not Found
        if response.status_code == 404:
            raise CharacterNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response
