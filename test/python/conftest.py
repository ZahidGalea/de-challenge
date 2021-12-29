import configparser
import pytest
from logging import getLogger
from logging.config import fileConfig

fileConfig('logging_config.ini')
TEST_INFRA_DECLARATION_JSON = "./ltdc-iac/environments/wom-control-tower-dev/variable_declaration.tfvars.json"


@pytest.fixture(scope='session')
def logger():
    return getLogger()


@pytest.fixture()
def context():
    class Context(object):
        pass

    context = Context()
    return context


@pytest.fixture(scope='session')
def infraestructure_config_file(logger) -> dict:
    infra_config = configparser.RawConfigParser()
    infra_config.read(f'src/resources/infra.ini')
    infra_dict = dict(infra_config)
    return infra_dict


@pytest.fixture(scope='session')
def gcp_storage_client():
    from google.cloud.storage import Client
    return Client()


@pytest.fixture(scope='session')
def gcp_pubsub_publisher_client():
    from google.cloud.pubsub_v1 import PublisherClient
    return PublisherClient()


@pytest.fixture(scope='session')
def gcp_bigquery_client():
    from google.cloud.bigquery import Client
    return Client()


def pytest_bdd_before_scenario(request, feature, scenario):
    pass
    # First clean everything...
    # clean_everything_please()


def pytest_bdd_after_scenario(request, feature, scenario):
    pass
    # clean_everything_please()
