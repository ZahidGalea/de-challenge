import re
from logging import getLogger
import os


def gcs_storage_upload_blob(bucket_name, source_file_name, destination_blob_name, logger=getLogger()):
    from google.cloud import storage
    gcp_storage_client = storage.Client()
    try:
        bucket = gcp_storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logger.info("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
    except Exception as e:
        logger.warning("Upload File Failed!")
        logger.fatal(e)
        return False
    return True


def clean_all_blobs_in_bucket(bucket_name):
    from google.cloud import storage
    gcp_storage_client = storage.Client()
    try:
        blobs = gcp_storage_client.list_blobs(bucket_name)
        if blobs:
            for blob in blobs:
                blob.delete()
    except Exception as e:
        return e
    return True


def clean_all_tables_in_dataset(dataset_name):
    from google.cloud.bigquery.client import Client
    gcp_bigquery_client = Client()
    try:
        tables = list(gcp_bigquery_client.list_tables(dataset_name))  # Make an API request(s).
        if tables:
            for table in tables:
                gcp_bigquery_client.delete_table(table.reference, not_found_ok=True)  # Make an API request.
    except Exception as e:
        return e


def table_exists(dataset_name, table):
    from google.cloud.bigquery.client import Client
    gcp_bigquery_client = Client()
    for table_ref in gcp_bigquery_client.list_tables(dataset_name):
        if table_ref.full_table_id.split(".")[-1] == table:
            return True
    return False


def blob_exists(bucket_name, file_name):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return storage.Blob(bucket=bucket, name=file_name).exists()


def blob_pattern_exists(bucket_name, file_pattern):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    for blob in storage_client.list_blobs(bucket):
        if re.search(file_pattern, blob.name):
            return True
    return False


def workflow_exists(workflow_parent_path, workflow_to_check_name):
    from google.cloud.workflows import WorkflowsClient
    # projects/{project}/locations/{location}
    client = WorkflowsClient()
    for workflow in client.list_workflows(parent=workflow_parent_path):
        if workflow.name.split("/")[-1] == workflow_to_check_name:
            return True
    return False


def request_a_cloud_function_http(function_path: str, data: dict):
    import requests
    response = requests.post(url=function_path, json=data)
    return response


def upload_folder_to_gcs(bucket_name, target_prefix, source_folder, logger=getLogger()):
    from google.cloud import storage
    gcp_storage_client = storage.Client()
    for root, dirs, files in os.walk(source_folder):
        try:
            for file in files:
                bucket = gcp_storage_client.bucket(bucket_name)
                target_blob = f'{target_prefix}/{file}'
                source_file = f'{root}/{file}'

                blob = bucket.blob(target_blob)
                blob.upload_from_filename(source_file)

                logger.info("File {} uploaded to {}.".format(source_file, target_blob))

        except Exception as e:
            logger.warning("Folder File Failed on upload!")
            logger.fatal(e)
            return False
        return True
