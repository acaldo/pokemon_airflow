from airflow.decorators import dag, task
from datetime import datetime
from airflow.models.baseoperator import chain

@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['pokemon']
)
def pokemon():
    @task.external_python(python='/usr/local/airflow/poke_venv/bin/python')
    def extract_pokemon_name():
        import asyncio
        from include.extract import pokemon_full,get_pokemon_stats
        limit = 1000
        offset = 0
        function = get_pokemon_stats
        url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}"
        data = asyncio.run(pokemon_full(limit, offset, url,function))
        #return data
        data.to_csv('include/dataset/pokemon.csv',index=False)
    
    extract_pokemon_name()

    @task.external_python(python='/usr/local/airflow/poke_venv/bin/python')
    def extract_pokemon_species():
        import asyncio
        from include.extract import pokemon_full,get_pokemon_species
        limit = 1000
        offset = 0
        function = get_pokemon_species
        url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}"
        data = asyncio.run(pokemon_full(limit, offset, url,function))
        #return data
        data.to_csv('include/dataset/species.csv',index=False)

    extract_pokemon_species()

pokemon()
