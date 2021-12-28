import base64
import pytest
from unittest import mock

from src.main.python.google_cloud_functions.workflow_trigger import main as workflow_trigger_main
from src.test.python.basetest import TestBase


class TestIntegration(TestBase):

    def setUp(self) -> None:
        self.config.pubsub_function_event = None

        # Mock for Google cloud functions triggered by pubsub - context
        mock_context = mock.Mock()
        mock_context.event_id = '617187464135194'
        mock_context.timestamp = '2019-07-15T22:09:03.761Z'
        mock_context.resource = {
            'name': 'projects/my-project/topics/my-topic',
            'service': 'pubsub.googleapis.com',
            'type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
        }

        self.config.pubsub_function_context = mock_context

    @pytest.mark.integrationtest
    def test_workflow_trigger(self):
        name = '{"bucket":"gs://bucket/test","name":"result.csv"}'
        self.config.pubsub_function_event = {'data': base64.b64encode(name.encode())}

        assert workflow_trigger_main.main(event=self.config.pubsub_function_event,
                                          context=self.config.pubsub_function_context)

    @pytest.mark.unittest
    def test_file_patterns(self):
        files_arrived = ["testing_20202031.csv", "3123_testing#.csv", "&&testing.csv23"]
        yaml_relation_file_identifier = 'testing'
        raw_bucket_file_identifier = 'testingcsv'
        for file in files_arrived:
            assert datalake_indexer_build_file_identifier(file) == raw_bucket_file_identifier
            assert workflow_build_file_identifier(file) == yaml_relation_file_identifier
