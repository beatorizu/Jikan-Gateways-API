from controller.core import JikanGatewaysAPI, ImageViewer
from model.character import Character
from model.manga import Manga
from model.anime import Anime
import requests

s = JikanGatewaysAPI(requests)

all_char = list()
for character in s.search_character('shouta aizawa').json().get('results'):
    all_char.append(Character(character))

all_anime = list()
for anime in s.search_anime('Boku No Hero').json().get('results'):
    all_anime.append(Anime(anime))

all_manga = list()
for manga in s.search_manga('Boku No Hero').json().get('results'):
    all_manga.append(Manga(manga))

all_anime_of_season = list()
for anime in s.list_animes_from_season(2018, 'winter').json().get('anime'):
    all_anime_of_season.append(Anime(anime))

works = s.search_person_works("junichi")
print(works)
print(all_char[0].image_url)
img = ImageViewer(all_char[0].image_url, requests)
print(all_anime[0].title)
print(all_manga[0].title)
print(all_anime_of_season[0].title)
img.print_picture()
