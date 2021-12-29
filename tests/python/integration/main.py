import time

from pytest_bdd import scenario, given, then, parsers
from tests.python.utils.resources_handler import workflow_exists, blob_exists, gcs_storage_upload_blob


@scenario('datapipeline/pipeline_framework.feature',
          'El archivo result.csv llega al bucket landing y se ejecuta la ETL')
def test_workflow_trigger(context):
    pass


@given(parsers.parse("el workflow {workflow_name} deployado en GCP"))
def step_impl(context, workflow_name, infraestructure_config_file, logger):
    logger.info('Check if the workflow exists')
    parent_path = f'projects/{infraestructure_config_file["TEST"]["project_id"]}' \
                  f'/locations/us-central1'
    assert workflow_exists(workflow_parent_path=parent_path,
                           workflow_to_check_name=workflow_name)


@given(parsers.parse("el template {dataflow_template} en un bucket de artefactos"))
def step_impl(context, infraestructure_config_file, dataflow_template, logger):
    logger.info('Check if the template exists in the GCS Bucket')
    assert blob_exists(bucket_name=infraestructure_config_file["TEST"]["artifacts_bucket"],
                       file_name=dataflow_template)


@given(
    parsers.parse("el archivo {path_test_data_file} en un bucket landing con el nombre {destiny_file}"))
def step_impl(context, infraestructure_config_file, path_test_data_file, destiny_file, logger):
    logger.info('Uploading file to landing')
    assert gcs_storage_upload_blob(bucket_name=infraestructure_config_file["TEST"]["landing_bucket"],
                                   destination_blob_name=destiny_file,
                                   source_file_name=path_test_data_file)


@then(parsers.parse("se valida el archivo consolidado en raw con el nombre {file_result_in_raw}"))
def step_impl(context, infraestructure_config_file, file_result_in_raw, logger):
    time.sleep(3)
    logger.info('Evaluating if the file exists in raw bucket')
    assert blob_exists(bucket_name=infraestructure_config_file["TEST"]["raw_bucket"],
                       file_name=file_result_in_raw)
    logger.info('It exists.')


@then(parsers.parse("se valida la existencia de la tabla {modelo} en el dataset {dataset} con los datos del archivo"))
def step_impl(context, modelo, dataset):
    NotImplementedError('Not implemented')


@then(parsers.parse("se valida la existencia de los {lista_archivos} en el bucket de analytics"))
def step_impl(context, lista_archivos):
    NotImplementedError('Not implemented')
