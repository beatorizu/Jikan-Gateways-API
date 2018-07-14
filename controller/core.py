import requests


class JikanGatewaysAPI(object):

    URL = 'https://api.jikan.moe/'

    def search_data(self):
        return requests.get(self.URL)
