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
    @task.external_python(python='/usr/local/airflow/poke_venv/bin/python',multiple_outputs=True)
    def extract_pokemon_name():
        import asyncio
        from include.extract import check
        limit = 1000
        offset = 0
        url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}"
        data = asyncio.run(check(limit, offset, url))
        #return data
        data.to_csv('include/dataset/pokemon.csv',index=False)
    
    extract_pokemon_name()

pokemon()
