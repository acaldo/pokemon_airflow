import asyncio
import aiohttp
import json
import pandas as pd

from include.DTO.pokemon_stats_dto import PokemonStatsDTO
from include.DTO.pokemon_species_dto import PokemonSpeciesDTO


async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_pokemon_name(session, url):
    data = await fetch_data(session, url)
    return [pokemon['url'] for pokemon in data['results']]


async def get_pokemon_stats(session, url):
    data = await fetch_data(session, url)
    id = data['id']
    name = data['name']
    types = data['types'][0]['type']['name']
    types2 = data['types'][1]['type']['name'] if len(
        data['types']) > 1 else None
    weight = data['weight']
    height = data['height']
    hp = data['stats'][0]['base_stat']
    attack = data['stats'][1]['base_stat']
    defense = data['stats'][2]['base_stat']
    sp_atk = data['stats'][3]['base_stat']
    sp_def = data['stats'][4]['base_stat']
    speed = data['stats'][5]['base_stat']
    moves = [(move['move']['name'], move['move']['url'], move['move']
              ['url'].rstrip('/').split('/')[-1]) for move in data['moves']]
    pokemon_stats = {
        'id': id,
        'name': name,
        'types': types,
        'types2': types2,
        'moves': moves,
        'weight': weight,
        'height': height,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'sp_atk': sp_atk,
        'sp_def': sp_def,
        'speed': speed
    }
    return pokemon_stats


async def get_pokemon_species(session, url):
    data = await fetch_data(session, url)
    return PokemonSpeciesDTO(
        data['id'],
        data['name'],
        data['gender_rate'],
        data['base_happiness'],
        data['is_baby'],
        data['is_legendary'],
        data['is_mythical'],
        data['hatch_counter'],
        data['has_gender_differences'],
        data['forms_switchable']
    )


async def pokemon_full(limit=1, offset=0, url=None, function=None):
    async with aiohttp.ClientSession() as session:
        pokemon_name_url = await fetch_pokemon_name(session, url)
        tasks = [function(session, name) for name in pokemon_name_url]
        pokemon_full = await asyncio.gather(*tasks)
        df = pd.DataFrame(pokemon_full)
        return df


def main():
    limit = 2
    offset = 0
    function = get_pokemon_stats
    url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}"
    data = asyncio.run(pokemon_full(limit, offset, url, function))
    # return data
    data.to_csv('include/dataset/pokemon.csv', index=False)


if __name__ == '__main__':
    main()


async def get_pokemon_stats(session, url):
    data = await fetch_data(session, url)
    moves = [(move['move']['name'], move['move']['url'], move['move']
              ['url'].rstrip('/').split('/')[-1]) for move in data['moves']]
    pokemon_stats = PokemonStatsDTO(
        data['id'],
        data['name'],
        data['types'][0]['type']['name'],
        data['types'][1]['type']['name'] if len(data['types']) > 1 else None,
        moves,
        data['weight'],
        data['height'],
        data['stats'][0]['base_stat'],
        data['stats'][1]['base_stat'],
        data['stats'][2]['base_stat'],
        data['stats'][3]['base_stat'],
        data['stats'][4]['base_stat'],
        data['stats'][5]['base_stat']
    )
    # print(pokemon_stats)
    print(asdict(pokemon_stats))
    return asdict(pokemon_stats)


async def get_pokemon_species(session, url):
    data = await fetch_data(session, url)
    return PokemonSpeciesDTO(
        data['id'],
        data['name'],
        data['gender_rate'],
        data['base_happiness'],
        data['is_baby'],
        data['is_legendary'],
        data['is_mythical'],
        data['hatch_counter'],
        data['has_gender_differences'],
        data['forms_switchable']
    )
