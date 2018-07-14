import requests
from urllib.parse import urlencode


class JikanGatewaysAPI(object):

    URL = 'https://api.jikan.moe/'

    def search_data(self):
        return requests.get(self.URL)

    def search_character(self, name):
        resource = 'search/character?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        return requests.get(full_url)
