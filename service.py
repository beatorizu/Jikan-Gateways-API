from controller.core import JikanGatewaysAPI
from model.character import Character
import requests

s = JikanGatewaysAPI(requests)
all_in = list()
for character in s.search_character('shouta aizawa').json().get('results'):
    all_in.append(Character(character))

print(all_in[0].name)