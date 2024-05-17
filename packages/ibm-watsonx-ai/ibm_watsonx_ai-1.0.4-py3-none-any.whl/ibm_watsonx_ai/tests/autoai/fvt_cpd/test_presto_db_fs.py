#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import unittest
from copy import copy
from unittest.mock import Mock, patch, MagicMock

from ibm_watsonx_ai.tests.utils import get_wml_credentials
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.helpers import DataConnection, DatabaseLocation


class TestPrestoConnection(unittest.TestCase):

    def setUp(self) -> None:
        self.database_name = "presto"
        self.schema_name = "test_schema"
        self.table_name = "test_table"
        self.catalog_name = "test_catalog"
        self.credentials = get_wml_credentials()
        self.api_client = APIClient(credentials=copy(self.credentials))

    def test_if_proper_arguments_are_provided(self):
        self.api_client.connections = Mock()
        self.api_client.connections.get_id.return_value = 'some_uid'

        self.connection_id = self.api_client.connections.get_id()
        self.api_client.default_project_id = "some_space_id"

        data_connection = DataConnection(
            connection_asset_id=self.connection_id,
            location=DatabaseLocation(
                schema_name=self.schema_name,
                table_name=self.table_name,
                catalog_name=self.catalog_name
            )
        )
        data_connection.set_client(self.api_client)
        with patch('ibm_watsonx_ai.helpers.connections.flight_service.flight') as flight_client:
            with patch('ibm_watsonx_ai.helpers.connections.flight_service.FlightConnection.create_logical_batch') as create_logical_batch_method:
                flight_client.authenticate.return_value = True
                create_logical_batch_method.return_value = []
                flight_client.FlightClient().get_flight_info.return_value = MagicMock()

                _ = data_connection.read()
                flight_client.FlightDescriptor.for_command.assert_called_with(
                    '{"num_partitions": 4, "batch_size": 10000, '
                    '"interaction_properties": {"schema_name": "test_schema", "table_name": "test_table", '
                    '"catalog_name": "test_catalog"}, "project_id": "some_space_id", "asset_id": "some_uid"}')

    def test_if_catalog_name_is_propagated_if_none(self):
        self.api_client.connections = Mock()
        self.api_client.connections.get_id.return_value = 'some_uid'

        self.connection_id = self.api_client.connections.get_id()
        self.api_client.default_project_id = "some_space_id"

        data_connection = DataConnection(
            connection_asset_id=self.connection_id,
            location=DatabaseLocation(
                schema_name=self.schema_name,
                table_name=self.table_name,
            )
        )
        assert data_connection.location.to_dict() == {'schema_name': self.schema_name, 'table_name': self.table_name}
        data_connection.set_client(self.api_client)
        with patch('ibm_watsonx_ai.helpers.connections.flight_service.flight') as flight_client:
            with patch('ibm_watsonx_ai.helpers.connections.flight_service.FlightConnection.create_logical_batch') as create_logical_batch_method:
                flight_client.authenticate.return_value = True
                create_logical_batch_method.return_value = []
                flight_client.FlightClient().get_flight_info.return_value = MagicMock()

                _ = data_connection.read()
                flight_client.FlightDescriptor.for_command.assert_called_with(
                    '{"num_partitions": 4, "batch_size": 10000, '
                    '"interaction_properties": {"schema_name": "test_schema", "table_name": "test_table"}, '
                    '"project_id": "some_space_id", "asset_id": "some_uid"}')


if __name__ == '__main__':
    unittest.main()
