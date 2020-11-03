
from io import BytesIO
from tkinter import Button, Label, Tk

from controller.static import TYPE_GENRE
from urllib.parse import urlencode

import numpy as np
from matplotlib.pyplot import imshow
from PIL import Image, ImageTk

                         MangaNotFoundException, ServiceUnavailable)

from controller.exceptions import (CharacterNotFoundException,
                                   AnimeNotFoundException,
                                   MangaNotFoundException,
                                   TopNotFoundException,
                                   PersonNotFoundException,
                                   SeasonNotFoundException,
                                   ServiceUnavailable)

from PIL import Image
from io import BytesIO


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

    def search_anime(self, name, genre=None):

        resource = 'v3/search/anime?'
        genre_id = TYPE_GENRE['anime']

        params = {"q": name}

        if genre is not None:
            if str(genre).isdigit():
                params.update({"genre": genre})
            else:
                genre = genre_id.get(genre,None)



        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode(params)

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

    def search_manga(self, name, genre=None):
        resource = 'v3/search/manga?'
        genre_id = TYPE_GENRE['manga']

        params = {"q": name}

        if genre is not None:
            if str(genre).isdigit():
                params.update({"genre": genre})
            else:
                genre = genre_id.get(genre,None)


        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode(params)

        full_url = f'{self.URL}{resource}{query_string}'

        print(full_url)

        response = self.client.get(full_url)


        # Not Found
        if response.status_code == 404:
            raise MangaNotFoundException(name)

    

    def delete_unused_entries(self, item):
        unused_entries = ['request_hash', 'request_cached', 'request_cache_expiry', 'url',
                          'image_url', 'website_url', 'anime_staff_positions']

        for entries in unused_entries:
            item.pop(entries, None)

        return item

    def search_person_works(self, name):
        resource = 'v3/search/people?'

        # traduz nosso dicionário python nos parametros de busca HTTP
        query_string = urlencode({'q': name})

        full_url = f'{self.URL}{resource}{query_string}'

        response = self.client.get(full_url)
        print(full_url)

        # Not Found
        if response.status_code == 404:
            raise MangaNotFoundException(name)
        # Service Unavailable
        elif response.status_code == 503:
            raise ServiceUnavailable()

        response = response.json()

        all_persons_id = list()

        for p in response.get('results'):
            all_persons_id.append(p.get('mal_id'))

        results = list()
        resource = 'v3/person/'

        for person in all_persons_id:
            full_url = f'{self.URL}{resource}{person}'
            rs = self.client.get(full_url).json()
            rs = self.delete_unused_entries(rs)
            results.append(rs)

        return results


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


    def get_top_mal(self, top_type):
        resource = 'v3/top/'

        # traduz nosso dicionário python nos parametros de busca HTTP

        full_url = f'{self.URL}{resource}{top_type}'

        print(full_url)

        response = self.client.get(full_url)
        # Not Found
        if response.status_code == 404 or response.status_code == 400:
            raise TopNotFoundException()
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

