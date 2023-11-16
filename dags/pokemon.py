from airflow.decorators import dag, task
from datetime import datetime
from airflow.models.baseoperator import chain

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType


from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig


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
        from include.extract import pokemon_full, get_pokemon_stats
        limit = 1292
        offset = 0
        function = get_pokemon_stats
        url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}"
        data = asyncio.run(pokemon_full(limit, offset, url, function))
        # return data
        data.to_csv('include/dataset/pokemon.csv', index=False)

    # extract_pokemon_name()

    @task.external_python(python='/usr/local/airflow/poke_venv/bin/python')
    def extract_pokemon_species():
        import asyncio
        from include.extract import pokemon_full, get_pokemon_species
        limit = 1292
        offset = 0
        function = get_pokemon_species
        url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}"
        data = asyncio.run(pokemon_full(limit, offset, url, function))
        # return data
        data.to_csv('include/dataset/species.csv', index=False)

    # extract_pokemon_species()

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_csv_to_gcs",
        src='include/dataset/*.csv',
        dst='raw/',
        bucket='acaldo_pokemon',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_retail_dataset",
        dataset_id='pokemon',
        gcp_conn_id='gcp',
        location='us-east1',
    )

    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://acaldo_pokemon/raw/species.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='species',
            conn_id='gcp',
            metadata=Metadata(schema='pokemon')
        ),
        use_native_support=False,
    )
    gcs_to_raw1 = aql.load_file(
        task_id='gcs_to_raw1',
        input_file=File(
            'gs://acaldo_pokemon/raw/pokemon.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='pokemon',
            conn_id='gcp',
            metadata=Metadata(schema='pokemon')
        ),
        use_native_support=False,
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        )
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    chain(
        [
            extract_pokemon_name(),
            extract_pokemon_species()
        ],
        upload_csv_to_gcs,
        create_retail_dataset,
        [
            gcs_to_raw,
            gcs_to_raw1
        ],
        check_load(),
        transform,
        check_transform()

    )


pokemon()
