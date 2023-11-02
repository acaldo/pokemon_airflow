import requests
import json


def extract_pokemon_name():
    pokemon_name = []
    limit = 10
    offset = 0
    API = "https://pokeapi.co/api/v2/pokemon/" + \
        '?limit=' + str(limit) + '&offset=' + str(offset)
    print(API)

    response = requests.get(
        API)
    data = json.loads(response.text)
    for pokemon in data['results']:
        pokemon_name.append(pokemon['name'])
    # print(pokemon_name)
    # return pokemon_name
    pokemon_full = []
    for name in pokemon_name:
        p = get_pokemon_stats(name)
        pokemon_full.append(p)

    print(pokemon_full)


def get_pokemon_stats(name):
    API = "https://pokeapi.co/api/v2/pokemon/" + \
        name
    response = requests.get(
        API)
    data = json.loads(response.text)

    order = data['order']
    pokemon = data['name']
    type1 = data['types'][0]['type']['name']
    if len(data['types']) > 1:
        type2 = data['types'][1]['type']['name']
    else:
        type2 = None

    pokemonDTO = {
        'id': order,
        'name': pokemon,
        'type1': type1,
        'type2': type2

    }
    # json dump
    return pokemonDTO
    # print(pokemonDTO)
    # print(json.dumps(response, indent=4))
