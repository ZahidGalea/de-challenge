import base64
import json
import os
import re
from datetime import datetime

from google.cloud.workflows.executions_v1.services.executions import async_client
from google.cloud.workflows.executions_v1.types import executions

import configparser


def build_file_identifier(file_name):
    return ''.join(filter(str.isalpha, file_name.split(".")[0]))


def get_config_that_matches(string, workflows_dict: dict):
    default_section = None
    for workflow, section in workflows_dict.items():
        if workflow == "DEFAULT":
            default_section = section
            continue
        if re.search(pattern=section["pattern"], string=string):
            return section
    return default_section


def main(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    gcf_syspath = os.path.dirname(__file__)
    runcontext_gcp_project_id = os.environ.get("GCP_PROJECT")
    runcontext_gcp_region = os.environ.get("FUNCTION_REGION")
    runcontext_environment = os.environ.get("ENVIRONMENT")
    if runcontext_environment not in ["PROD", "TEST"]:
        raise ValueError('The environment variable must be PROD or TEST')
    if not runcontext_gcp_region:
        raise ValueError('The GCP Region must be implemented')
    if not runcontext_gcp_project_id:
        raise ValueError('The project ID must be implemented')

    # It reads the workflows that handles the patterns and what to execute
    workflows_config = configparser.RawConfigParser()
    workflows_config.read(f'{gcf_syspath}/workflows.ini')
    workflows_dict = dict(workflows_config)

    # It read the infraestructure file required to know the structure of the project
    infra_config = configparser.RawConfigParser()
    infra_config.read(f'{gcf_syspath}/infra.ini')
    infra_dict = dict(infra_config)

    if "PROD" not in infra_dict:
        raise OSError("Failed to load infraestructure dictionary")

    # # Opens workflows.properties
    # with open(f'{gcf_syspath}/workflows.properties', 'r+') as patterns:
    #     workflows_dict = json.loads(patterns.read())

    # First variable definitions
    data = base64.b64decode(event['data']).decode('utf-8')
    data_dict = json.loads(data)
    file_bucket = data_dict["bucket"]
    file_path = data_dict["name"]
    file_name = file_path.split("/")[-1]

    # It looks for the workflow config that matches the first pattern
    file_config = get_config_that_matches(string=file_name,
                                          workflows_dict=workflows_dict)

    ############## ARGUMENTS PREPARATION ##########################

    datetime_now = datetime.now().strftime("%Y%m%d%H%M%S")
    if file_config.name == "DEFAULT":
        workflows_arguments = {
            "source_bucket": f'{file_bucket}',
            "source_file": f'{file_name}',
            "raw_bucket": infra_config[runcontext_environment]["raw_bucket"]
        }
    else:
        workflows_arguments = {
            "source_bucket": f'{file_bucket}',
            "source_file": f'{file_name}',
            "raw_bucket": infra_config[runcontext_environment]["raw_bucket"],
            "raw_prefix": file_config["raw_prefix"],
            "analytics_bucket": infra_config[runcontext_environment]["analytics_bucket"],
            "staging_dataset": infra_config[runcontext_environment]["staging_dataset"],
            "artifacts_bucket": infra_config[runcontext_environment]["artifacts_bucket"],
            "temporary_bucket": infra_config[runcontext_environment]["temporary_bucket"],
            "execution_date": datetime_now
        }

    if "dataflow_job" in file_config:
        workflows_arguments["dataflow_template"] = file_config["dataflow_job"]

    ############## WORKFLOW EXECUTION    ##########################
    # Init the client
    workflow_client = async_client.ExecutionsClient()
    parent_path = "projects/{project}/locations/{location}/workflows/{workflow}"

    print('Generating Execution...')
    # Generates a definition with the arguments as parameters
    execution = executions.Execution(argument=json.dumps(obj=workflows_arguments))
    # Executes it
    print('Creating Execution')
    workflow_client.create_execution(parent=parent_path.format(project=runcontext_gcp_project_id,
                                                               location=runcontext_gcp_region,
                                                               workflow=file_config["workflow_to_trigger"]),
                                     execution=execution)

    print('Workflow execution ended')
    return True
