#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import pytest
from pandas import DataFrame

from ibm_watsonx_ai.connections import Connections
from ibm_watsonx_ai.metanames import ConnectionMetaNames
from ibm_watsonx_ai.href_definitions import HrefDefinitions

from ibm_watsonx_ai.wml_client_error import (
    MissingValue,
    ApiRequestFailure,
    MissingMetaProp,
    UnexpectedType,
)

from ibm_watsonx_ai.tests.unit.conftest import mock_data_from_requests


@pytest.mark.unittest
class TestConnections:
    """
    These tests cover:
    - method get_id
    - method create
    """

    url = "https://unit-tests.com"
    connection_id = "21032409-8a2d-461b-88be-bf9fb80d5b1c"
    get_response = {
        "resources": [
            {
                "entity": {
                    "name": "bigquery",
                    "type": "database",
                    "status": "active",
                },
                "metadata": {"asset_id": "039e5d1c-ba73-4b09-b742-14c1539b6cf9"},
            }
        ]
    }

    post_response = {
        "metadata": {
            "asset_id": "sample_asset_id",
            "asset_type": "sample_asset_type",
            "create_time": "2024-02-21T10:11:06.846Z",
            "usage": {"last_access_time": "2024-01-12T20:18:06.846Z"},
        },
        "entity": {
            "datasource_type": "sample_datasource_type2",
            "name": "sample_name2",
        },
    }

    @pytest.fixture(scope="function", name="connections")
    def fixture_connections(self, api_client_mock):
        connections = Connections(api_client_mock)
        api_client_mock.credentials.url = self.url
        api_client_mock.service_instance._href_definitions = HrefDefinitions(
            api_client_mock
        )
        connections.ConfigurationMetaNames = ConnectionMetaNames()
        return connections

    def test_get_id_valid(self, connections):
        metadata = {
            "entity": {"type": "prompt_tuning"},
            "metadata": {"id": "sample_id", "created_at": "2024-02-21T10:11:06.846Z"},
        }

        connection_id = connections.get_id(metadata)

        assert connection_id == "sample_id"

    def test_get_id_empty_metadata(self, connections):
        with pytest.raises(MissingValue) as e:
            connections.get_id(connection_details={})

        assert e.value.error_msg == 'No "connection_details.metadata" provided.'

    def test_get_id_invalid_metadata(self, connections):
        metadata = {
            "entity": {"type": "prompt_tuning"},
            "metadata": {"created_at": "2024-02-21T10:11:06.846Z"},
        }
        with pytest.raises(MissingValue) as e:
            connections.get_id(connection_details=metadata)

        assert e.value.error_msg == 'No "connection_details.metadata.id" provided.'

    def test_create_valid(self, connections, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, self.get_response, session=True
        )
        mock_post = mock_data_from_requests("post", mocker, self.post_response, 201)

        get_calls = mocker.call(self.url + "/v2/datasource_types", headers={})
        post_calls = mocker.call(
            self.url + "/v2/connections",
            headers={},
            json={
                "name": "sample_name",
                "datasource_type": "sample_datasource_type",
                "properties": {},
                "origin_country": "US",
            },
            params={},
        )

        connection_details = connections.create(
            {
                connections.ConfigurationMetaNames.NAME: "sample_name",
                connections.ConfigurationMetaNames.DATASOURCE_TYPE: "sample_datasource_type",
                connections.ConfigurationMetaNames.PROPERTIES: {},
            }
        )

        mock_get.assert_has_calls([get_calls])
        mock_post.assert_has_calls([post_calls])
        assert isinstance(connection_details, dict), "connection_details are not `dict`"

    def test_create_failed(self, connections, mocker):
        mock_data_from_requests("get", mocker, self.get_response, session=True)
        mock_data_from_requests("post", mocker, self.post_response, status_code=503)

        with pytest.raises(ApiRequestFailure):
            connections.create(
                {
                    connections.ConfigurationMetaNames.NAME: "sample_name",
                    connections.ConfigurationMetaNames.DATASOURCE_TYPE: "sample_datasource_type",
                    connections.ConfigurationMetaNames.PROPERTIES: {},
                }
            )

    def test_create_no_name_specified(self, connections, mocker):
        mock_data_from_requests("get", mocker, self.get_response, session=True)
        mock_data_from_requests("post", mocker, self.post_response, status_code=201)
        msg = "Missing meta_prop with name: 'name'."

        with pytest.raises(MissingMetaProp) as e:
            connections.create(
                {
                    connections.ConfigurationMetaNames.DATASOURCE_TYPE: "sample_datasource_type",
                    connections.ConfigurationMetaNames.PROPERTIES: {},
                }
            )

        assert msg in e.value.error_msg, f"Invalid error msg: {e.value.error_msg}"

    def test_create_no_datasource_type_specified(self, connections, mocker):
        mock_data_from_requests("get", mocker, self.get_response, session=True)
        mock_data_from_requests("post", mocker, self.post_response, status_code=201)
        msg = "Missing meta_prop with name: 'datasource_type'."

        with pytest.raises(MissingMetaProp) as e:
            connections.create(
                {
                    connections.ConfigurationMetaNames.NAME: "sample_name",
                    connections.ConfigurationMetaNames.PROPERTIES: {},
                }
            )

        assert msg in e.value.error_msg, f"Invalid error msg: {e.value.error_msg}"

    def test_delete_valid(self, connections, mocker):
        mock_delete = mock_data_from_requests("delete", mocker, status_code=204)

        call_delete = mocker.call(
            self.url + "/v2/connections/" + self.connection_id,
            params={},
            headers={},
        )

        connections.delete(self.connection_id)

        mock_delete.assert_has_calls([call_delete])

    def test_delete_invalid_id_type(self, connections):
        error_msg = "Unexpected type of 'connection_id'"

        with pytest.raises(UnexpectedType) as e:
            connections.delete({"connection_id": self.connection_id})  # must be str

        assert error_msg in e.value.error_msg, f"Invalid error msg: {e.value.error_msg}"

    def test_list_datasource_types(self, connections, mocker):
        mock_get = mock_data_from_requests("get", mocker, self.get_response)
        call_get = mocker.call(self.url + "/v2/datasource_types", headers={})

        datasource_types = connections.list_datasource_types()

        mock_get.assert_has_calls([call_get])

        assert isinstance(
            datasource_types, DataFrame
        ), "Listed datasource types is not DataFrame"
        assert (
            datasource_types.NAME.iloc[0] == "bigquery"
        ), "Invalid casting of `name` field"
        assert (
            datasource_types.TYPE.iloc[0] == "database"
        ), "Invalid casting of `type` field"
        assert (
            datasource_types.DATASOURCE_ID.iloc[0]
            == "039e5d1c-ba73-4b09-b742-14c1539b6cf9"
        ), "Invalid casting of `datasource` field"
        assert (
            datasource_types.STATUS.iloc[0] == "active"
        ), "Invalid casting of `status` field"
