from io import BytesIO
from tkinter import Button, Label, Tk
from urllib.parse import urlencode

from PIL import Image, ImageTk

from controller.exceptions import (AnimeNotFoundException,
                                   CharacterNotFoundException,
                                   MangaNotFoundException,
                                   PersonNotFoundException,
                                   SeasonNotFoundException, ServiceUnavailable)


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

    def search_anime(self, name,):
        resource = 'v3/search/anime?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise AnimeNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response

    def list_animes_from_season(self, year, season):
        resource = 'v3/season/'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = f'{year}/{season}'

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise SeasonNotFoundException(year, season)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response

    def search_manga(self, name):
        resource = 'v3/search/manga?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise MangaNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response

    def search_person(self, name):
        resource = 'v3/search/people?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise PersonNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

    def search_manga(self, name):
        resource = 'v3/search/manga?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise MangaNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response

    def search_person(self, name):
        resource = 'v3/search/people?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)

        # Not Found
        if response.status_code == 404:
            raise PersonNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        return response


class ImageViewer:
    def __init__(self, image, client_http):
        self.image = image
        self.client = client_http

    def print_picture(self):
        response = self.client.get(self.image)

        image = Image.open(BytesIO(response.content))
        image.show()

    def image_viewer(self):

        response = self.client.get(self.image)

        image = Image.open(BytesIO(response.content))
        width, height = image.size
        root = Tk()
        root.title("Image Viewer")
        root.geometry(f"{width}x{height+35}")
        image = ImageTk.PhotoImage(image)

        label = Label(image=image)
        label.grid(row=1, column=0, columnspan=3)
        button_exit = Button(root, text="Exit", command=root.quit)
        button_exit.grid(row=5, column=1)

        root.mainloop()
