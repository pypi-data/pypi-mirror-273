#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import pytest
from typing import Literal
from pytest_mock import MockerFixture
from unittest.mock import Mock

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai._wrappers import requests
from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.training import Training
from ibm_watsonx_ai.repository import Repository
from ibm_watsonx_ai.service_instance import ServiceInstance
from ibm_watsonx_ai.href_definitions import HrefDefinitions
from ibm_watsonx_ai.hw_spec import HwSpec
from ibm_watsonx_ai.metanames import (
    HwSpecMetaNames,
    ModelMetaNames,
    TrainingConfigurationMetaNames,
)

from ibm_watsonx_ai.helpers import DataConnection, ContainerLocation, S3Connection


@pytest.fixture(scope="session", name="credentials")
def fixture_credentials():
    """
    Fixture responsible for loading sample credentials
        return:
            dict: Credentials for WX
    """
    return Credentials.from_dict({"url:": "fake_url"})


@pytest.fixture(scope="function", name="api_client_mock")
def fixture_api_client_mock(credentials, mocker):
    """
    Fixture responsible for setup API Client with random data.
        Args:
            credentials: credentials
            mocker: mocker needed for client
        return:
            APIClient Object:
    """
    api_client = mocker.Mock(spec=APIClient)

    api_client.default_space_id = None
    api_client.default_project_id = None
    api_client.token = "token"
    api_client._params.return_value = {}
    api_client._get_headers.return_value = {}
    api_client.CPD_version = 4.8
    api_client._use_fm_ga_api = True

    api_client.ICP_PLATFORM_SPACES = None
    api_client.CLOUD_PLATFORM_SPACES = None

    api_client.credentials = credentials
    api_client.credentials.url = "credentials_url"

    api_client.training = mocker.Mock(spec=Training)
    api_client.training.ConfigurationMetaNames = TrainingConfigurationMetaNames()

    api_client.repository = mocker.Mock(spec=Repository)
    api_client.repository.ModelMetaNames = ModelMetaNames()

    api_client.service_instance = mocker.Mock(spec=ServiceInstance)
    api_client.service_instance._credentials = credentials
    api_client.service_instance._href_definitions = mocker.Mock(spec=HrefDefinitions)
    api_client.service_instance._href_definitions.get_published_models_href.return_value = (
        "{}/v4/models"
    )
    api_client.service_instance._href_definitions.get_deployments_href.return_value = (
        "{}/v4/deployments"
    )
    api_client.service_instance._href_definitions.get_fm_deployment_generation_href.return_value = (
        "{}/ml/v1/deployments/{}/text/generation"
    )

    api_client.service_instance._href_definitions.get_fm_specifications_href.return_value = (
        "{}/ml/v1/foundation_model_specs"
    )

    api_client.hardware_specifications = mocker.Mock(spec=HwSpec)
    api_client.hardware_specifications.ConfigurationMetaNames = HwSpecMetaNames()

    return api_client


def mock_s3_connection(mock):
    data_conn = mock.Mock(spec=DataConnection)
    data_conn.location = mock.Mock(spec=ContainerLocation)
    data_conn.connection = mock.Mock(spec=S3Connection)
    return data_conn


def mock_get_details(mock, model_id="", auto_update_model="True", status=None):
    details_mocked = {
        "entity": {
            "model_id": model_id,
            "status": status if status else {},
            "auto_update_model": auto_update_model,
        }
    }
    mock.training.get_details.return_value = details_mocked
    return details_mocked


def mock_data_from_requests(
    api: Literal["post", "get", "delete"],
    mock: MockerFixture,
    json: dict | None = None,
    status_code: int = 200,
    session: bool = False,
):
    if json is None:
        json = {}

    RequestsMock.data[api] = json
    RequestsMock.error_code[api] = status_code

    if api == "delete":
        return mock.patch.object(
            requests, "delete", side_effect=RequestsMock.mocked_requests_delete
        )
    elif api == "post":
        return mock.patch.object(
            requests, "post", side_effect=RequestsMock.mocked_requests_post
        )
    else:
        return mock.patch.object(
            requests.Session if session else requests,
            "get",
            side_effect=RequestsMock.mocked_requests_get,
        )


class RequestsMock:
    data = {}
    error_code = {}

    def mocked_requests_get(*args, **kwargs):
        requests_get = Mock()
        requests_get.json.return_value = RequestsMock.data["get"]
        requests_get.status_code = RequestsMock.error_code["get"]
        return requests_get

    def mocked_requests_post(*args, **kwargs):
        requests_post = Mock()
        requests_post.json.return_value = RequestsMock.data["post"]
        requests_post.status_code = RequestsMock.error_code["post"]
        return requests_post

    def mocked_requests_delete(*args, **kwargs):
        requests_delete = Mock()
        requests_delete.json.return_value = RequestsMock.data["delete"]
        requests_delete.status_code = RequestsMock.error_code["delete"]
        return requests_delete
