from urllib.parse import urlencode
from controller.exceptions import CharacterNotFoundException


class JikanGatewaysAPI(object):

    URL = 'https://api.jikan.moe/'

    def __init__(self, client_http):
        self.client = client_http

    def search_data(self):
        return self.client.get(self.URL)

    def search_character(self, name):
        resource = 'search/character?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise CharacterNotFoundException(name)
        return response
