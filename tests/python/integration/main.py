import ast
import logging
import time
from datetime import datetime

from pytest_bdd import scenario, given, then, parsers
from tests.python.utils import resources_handler


@scenario('datapipeline/pipeline_framework.feature',
          'El archivo result.csv llega al bucket landing y se ejecuta la ETL')
def test_result_csv(context):
    pass


@scenario('datapipeline/pipeline_framework.feature',
          'El archivo consoles.csv llega al bucket landing y se ejecuta la ETL')
def test_consoles_csv(context):
    pass


@scenario('datapipeline/pipeline_framework.feature',
          'El archivo sindefinicion.csv llega al bucket landing y se ejecuta la ETL')
def test_sin_definicion(context):
    pass


@given(parsers.parse("el workflow {workflow_name} deployado en GCP"))
def step_impl(context, workflow_name, infraestructure_config_file, logger):
    logger.info('Check if the workflow exists')
    parent_path = f'projects/{infraestructure_config_file["TEST"]["project_id"]}' \
                  f'/locations/us-central1'
    assert resources_handler.workflow_exists(workflow_parent_path=parent_path,
                                             workflow_to_check_name=workflow_name)


@given(parsers.parse("el template {dataflow_template} en un bucket de artefactos"))
def step_impl(context, infraestructure_config_file, dataflow_template, logger):
    logger.info('Check if the template exists in the GCS Bucket')
    assert resources_handler.blob_exists(bucket_name=infraestructure_config_file["TEST"]["artifacts_bucket"],
                                         file_name=dataflow_template)


@given(
    parsers.parse("el archivo {path_test_data_file} en un bucket landing con el nombre {destiny_file}"))
def step_impl(context, infraestructure_config_file, path_test_data_file, destiny_file, logger):
    logger.info('Uploading file to landing')
    assert resources_handler.gcs_storage_upload_blob(bucket_name=infraestructure_config_file["TEST"]["landing_bucket"],
                                                     destination_blob_name=destiny_file,
                                                     source_file_name=path_test_data_file)


@then(parsers.parse("se valida el archivo consolidado en raw con el nombre {file_result_in_raw}"))
def step_impl(context, infraestructure_config_file, file_result_in_raw, logger):
    time.sleep(3)
    logger.info('Evaluating if the file exists in raw bucket')
    assert resources_handler.blob_exists(bucket_name=infraestructure_config_file["TEST"]["raw_bucket"],
                                         file_name=file_result_in_raw)
    logger.info('It exists.')


@then(parsers.parse("se valida la existencia de la tabla {modelo} en el dataset staging con los datos del archivo"))
def step_impl(context, modelo, infraestructure_config_file, logger):
    wait_time = 420
    logger.info(f'Waiting {wait_time} seconds')
    time.sleep(wait_time)
    assert resources_handler.table_exists(dataset_name=infraestructure_config_file["TEST"]["staging_dataset"],
                                          table=modelo)
    logger.info(f'Table exists.')


@then(parsers.parse("se valida la existencia de los {lista_patterns} en el bucket de analytics"))
def step_impl(context, lista_patterns, infraestructure_config_file, logger):
    lista_patterns = ast.literal_eval(lista_patterns)
    for pattern in lista_patterns:
        assert resources_handler.blob_pattern_exists(
            bucket_name=infraestructure_config_file["TEST"]["analytics_bucket"],
            file_pattern=pattern)
    logger.info('Files in analytics exists')
