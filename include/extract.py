import asyncio
import aiohttp
import json
import pandas as pd


async def fetch_pokemon_name(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return [pokemon['url'] for pokemon in data['results']]


async def get_pokemon_stats(session, name):
    url = name
    async with session.get(url) as response:
        data = await response.json()
        id = data['id']
        pokemon = data['name']
        type1 = data['types'][0]['type']['name']
        type2 = data['types'][1]['type']['name'] if len(
            data['types']) > 1 else None
        move_data = [{'move': move['move']['name'], 'url': move['move']['url'],
                      'id': move['move']['url'].rstrip('/').split('/')[-1]} for move in data['moves']]

        weight = data['weight']
        height = data['height']
        hp = data['stats'][0]['base_stat']
        attack = data['stats'][1]['base_stat']
        defense = data['stats'][2]['base_stat']
        sp_atk = data['stats'][3]['base_stat']
        sp_def = data['stats'][4]['base_stat']
        speed = data['stats'][5]['base_stat']

        pokemonDTO = {
            'id': id,
            'name': pokemon,
            'type1': type1,
            'type2': type2,
            'moves': move_data,
            'weight': weight,
            'height': height,
            'hp': hp,
            'attack': attack,
            'defense': defense,
            'sp_atk': sp_atk,
            'sp_def': sp_def,
            'speed': speed
        }
        return pokemonDTO


async def get_pokemon_species(session, name):
    uid = name.rstrip('/').split('/')[-1]
    url = f"https://pokeapi.co/api/v2/pokemon-species/{uid}"
    async with session.get(url) as response:
        data = await response.json()
        id = data['id']
        pokemon = data['name']
        gender_rate = data['gender_rate']
        base_happiness = data['base_happiness']
        is_baby = data['is_baby']
        is_legendary = data['is_legendary']
        is_mythical = data['is_mythical']
        hatch_counter = data['hatch_counter']
        has_gender_differences = data['has_gender_differences']
        forms_switchable = data['forms_switchable']

        speciesDTO = {
            'id': id,
            'name': pokemon,
            'gender_rate': gender_rate,
            'base_happiness': base_happiness,
            'is_baby': is_baby,
            'is_legendary': is_legendary,
            'is_mythical': is_mythical,
            'hatch_counter': hatch_counter,
            'has_gender_differences': has_gender_differences,
            'forms_switchable': forms_switchable
        }
        return speciesDTO


async def pokemon_full(limit=1, offset=0, url=None, function=None):

    async with aiohttp.ClientSession() as session:
        pokemon_name = await fetch_pokemon_name(session, url)
        tasks = [function(session, name) for name in pokemon_name]
        pokemon_full = await asyncio.gather(*tasks)
        df = pd.DataFrame(pokemon_full)
        # print(df)
        return df
