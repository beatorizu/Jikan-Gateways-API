from controller.core import JikanGatewaysAPI, ImageViewer
from model.character import Character
from model.anime import Anime
import requests

s = JikanGatewaysAPI(requests)
all_char = list()
for character in s.search_character('shouta aizawa').json().get('results'):
    all_char.append(Character(character))
all_anime = list()
for anime in s.search_anime('Boku No Hero').json().get('results'):
    all_anime.append(Anime(anime))

print(all_char[0].image_url)
img = ImageViewer(all_char[0].image_url,requests)
img.print_picture()
print(all_anime[0].title)