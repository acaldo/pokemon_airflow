import asyncio
import aiohttp
import json
import pandas as pd


async def fetch_pokemon_name(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return [pokemon['name'] for pokemon in data['results']]


async def get_pokemon_stats(session, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with session.get(url) as response:
        data = await response.json()
        id = data['id']
        pokemon = data['name']
        type1 = data['types'][0]['type']['name']
        type2 = data['types'][1]['type']['name'] if len(
            data['types']) > 1 else None
        move_names = {move['move']['name'] for move in data['moves']}
        weight = data['weight']
        height = data['height']
        hp=data['stats'][0]['base_stat']
        attack=data['stats'][1]['base_stat']
        defense=data['stats'][2]['base_stat']
        sp_atk=data['stats'][3]['base_stat']
        sp_def=data['stats'][4]['base_stat']
        speed=data['stats'][5]['base_stat']

        pokemonDTO = {
            'id': id,
            'name': pokemon,
            'type1': type1,
            'type2': type2,
            'moves': move_names,
            'weight': weight,
            'height': height,
            'hp':hp,
            'attack':attack,
            'defense':defense,
            'sp_atk':sp_atk,
            'sp_def':sp_def,
            'speed':speed
        }
        return pokemonDTO


async def check(limit=1, offset=0, url=None):

    async with aiohttp.ClientSession() as session:
        pokemon_name = await fetch_pokemon_name(session, url)
        tasks = [get_pokemon_stats(session, name) for name in pokemon_name]
        pokemon_full = await asyncio.gather(*tasks)
        df = pd.DataFrame(pokemon_full)
        # print(df)
        return df

if __name__ == '__main__':
    asyncio.run(check(limit, offset, url))
    """ df = pd.DataFrame(pokemon)
    print(df) """
