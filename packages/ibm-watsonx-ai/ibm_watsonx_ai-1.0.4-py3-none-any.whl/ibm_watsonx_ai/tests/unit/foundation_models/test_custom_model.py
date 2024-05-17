#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from typing import Generator

import pytest

from ibm_watsonx_ai.foundation_models.utils.utils import (
    get_custom_model_specs,
)
from ibm_watsonx_ai.foundation_models_manager import FoundationModelsManager

from ibm_watsonx_ai.models import Models
from ibm_watsonx_ai.hw_spec import HwSpec
from ibm_watsonx_ai.deployments import Deployments
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.wml_client_error import (
    WMLClientError,
    MissingMetaProp,
    InvalidValue,
)

from ibm_watsonx_ai.tests.unit.conftest import mock_data_from_requests


@pytest.mark.unittest
class TestCustomModel:
    """
    These tests cover:
    - utils method get_custom_model_spec
    - model store
    - hardware specification store
    - model deployment
    - model inference generate
    """

    model_name = "Mixtral-8x7B"
    model_asset_id = "33527417-5d33-4ecd-9acf-dbb604586a4f"
    deployment_id = "1e09f0d0-6656-4846-9877-04c90a9d25f5"
    get_custom_models_rsp = {"resources": [{"model_id": "Mixtral-8x7B"}]}


    def setup_model_inference(self, api_client_mock, mocker):
        response = {
            "results": [
                {
                    "generated_text": "\n\nSome answer",
                    "generated_token_count": 4,
                    "input_token_count": 9,
                    "stop_reason": "max_tokens",
                }
            ]
        }
        mock_post = mock_data_from_requests(
            "post", mocker, json=response, status_code=200
        )
        mock_get = mock_data_from_requests("get", mocker, json=response)

        api_client_mock.deployments = Deployments(api_client_mock)
        api_client_mock.foundation_models = FoundationModelsManager(api_client_mock)

        deployment_inference = ModelInference(
            deployment_id=self.deployment_id, api_client=api_client_mock
        )
        return mock_get, mock_post, deployment_inference

    def test_get_all_custom_models_spec(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, json=self.get_custom_models_rsp
        )

        model_specs = get_custom_model_specs(api_client=api_client_mock)

        mock_get.assert_called_once_with(
            "credentials_url/ml/v4/custom_foundation_models",
            params={"limit": 100},
            headers={},
        )
        api_client_mock._params.assert_called_once_with(skip_for_create=True, skip_userfs=True)

        assert "resources" in model_specs, "Specs do not contain `resources` field"

    def test_get_specific_custom_models_spec(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, json=self.get_custom_models_rsp
        )

        model_specs = get_custom_model_specs(
            api_client=api_client_mock, model_id=self.model_name
        )

        mock_get.assert_called_once_with(
            "credentials_url/ml/v4/custom_foundation_models",
            params={"limit": 100},
            headers={},
        )
        assert model_specs != {}, "Specs are empty"

    def test_get_invalid_custom_models_spec(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, json=self.get_custom_models_rsp
        )

        model_specs = get_custom_model_specs(
            api_client=api_client_mock, model_id="non_existing_model_name"
        )

        mock_get.assert_called_once_with(
            "credentials_url/ml/v4/custom_foundation_models",
            params={"limit": 100},
            headers={},
        )

        assert model_specs == {}, "Specs are not empty"

    def test_get_custom_models_spec_limit_valid(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, json=self.get_custom_models_rsp
        )

        model_specs = get_custom_model_specs(api_client=api_client_mock, limit=50)

        mock_get.assert_called_once_with(
            "credentials_url/ml/v4/custom_foundation_models",
            params={"limit": 50},
            headers={},
        )

        assert "resources" in model_specs, "Specs do not contain `resources` field"

    def test_get_custom_models_spec_limit_exceeded(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, json=self.get_custom_models_rsp
        )

        with pytest.raises(InvalidValue):
            get_custom_model_specs(api_client=api_client_mock, limit=201)

        mock_get.assert_not_called()

    def test_get_custom_models_spec_limit_below_one(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests("get", mocker)

        with pytest.raises(InvalidValue):
            get_custom_model_specs(api_client=api_client_mock, limit=0)

        mock_get.assert_not_called()

    def test_get_custom_models_spec_async(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests("get", mocker)

        model_specs_gen = get_custom_model_specs(
            api_client=api_client_mock, asynchronous=True
        )

        mock_get.assert_not_called()
        assert isinstance(
            model_specs_gen, Generator
        ), "`get_custom_model_specs` did not return Generator"

    def test_get_custom_models_spec_get_all(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests("get", mocker)
        api_client_mock.training._handle_response.return_value = {}

        model_specs = get_custom_model_specs(api_client=api_client_mock, get_all=True)

        mock_get.assert_called_once_with(
            url="credentials_url/ml/v4/custom_foundation_models",
            params={"limit": 100},
            headers={},
        )

        assert "resources" in model_specs, "Specs do not contain `resources` field"

    def test_store_model_valid(self, api_client_mock, mocker):
        response = {
            "entity": {"status": {"state": "ready"}},
            "metadata": {
                "name": "random_name",
                "id": self.model_asset_id,
            },
        }
        mock_data_from_requests("post", mocker, json=response, status_code=202)
        mock_data_from_requests("get", mocker, json=response)

        api_client_mock.default_space_id = ""

        metadata = {
            api_client_mock.repository.ModelMetaNames.NAME: "custom fm test",
            api_client_mock.repository.ModelMetaNames.SOFTWARE_SPEC_UID: "aaaaaaaa-bbbb-cccc-dddd-eeeeeeee",
            api_client_mock.repository.ModelMetaNames.TYPE: "custom_foundation_model_1.0",
        }
        models = Models(api_client_mock)

        stored_details = models.store(self.model_name, meta_props=metadata)

        api_client_mock.service_instance._href_definitions.get_published_models_href.assert_called()
        assert isinstance(
            stored_details, dict
        ), "`Models.store()` should not return empty dict"

    def test_store_model_cloud(self, api_client_mock):
        api_client_mock.default_project_id = "project_id"
        api_client_mock.CLOUD_PLATFORM_SPACES = True
        models = Models(api_client_mock)

        with pytest.raises(WMLClientError):
            models.store(
                self.model_name, meta_props={"type": "custom_foundation_model_1"}
            )

    def test_store_model_empty_metadata(self, api_client_mock):
        api_client_mock.default_project_id = "project_id"
        models = Models(api_client_mock)

        with pytest.raises(MissingMetaProp):
            models.store(self.model_name, meta_props={})

    def test_store_model_invalid_cpd_version(self, api_client_mock):
        api_client_mock.default_project_id = "project_id"
        api_client_mock.CPD_version = 4.7

        metadata = {
            api_client_mock.repository.ModelMetaNames.TYPE: "custom_foundation_model_1.0"
        }
        models = Models(api_client_mock)

        with pytest.raises(WMLClientError):
            models.store(self.model_name, meta_props=metadata)

    def test_store_model_invalid_metadata(self, api_client_mock):
        api_client_mock.default_project_id = "project_id"
        metadata = {
            api_client_mock.repository.ModelMetaNames.TYPE: "custom_foundation_model_1.0"
        }
        models = Models(api_client_mock)

        with pytest.raises(MissingMetaProp):
            models.store(self.model_name, meta_props=metadata)

    def test_store_hardware_spec_valid(self, api_client_mock, mocker):
        rsp = {
            "metadata": {
                "name": "HW SPEC from sdk",
                "id": "0bfee5c9-bd87-435e-8597-4df4e55c5218",
            }
        }
        mock_post = mock_data_from_requests("post", mocker, json=rsp, status_code=201)

        metadata = {
            api_client_mock.hardware_specifications.ConfigurationMetaNames.NAME: "HW SPEC from sdk",
            api_client_mock.hardware_specifications.ConfigurationMetaNames.NODES: {
                "cpu": {"units": "2"},
                "mem": {"size": "128Gi"},
                "gpu": {"num_gpu": 1},
            },
        }
        hardware_specifications = HwSpec(api_client_mock)

        hw_spec_details = hardware_specifications.store(metadata)

        api_client_mock.service_instance._href_definitions.get_hw_specs_href.assert_called_once()
        data = (
            '{"name": "HW SPEC from sdk", '
            '"nodes": {'
            '"cpu": {"units": "2"}, '
            '"mem": {"size": "128Gi"}, '
            '"gpu": {"num_gpu": 1}}'
            "}"
        )
        mock_post.assert_has_calls(
            [
                mocker.call(
                    mocker.ANY,
                    params={},
                    headers={},
                    data=data,
                )
            ]
        )
        assert isinstance(hw_spec_details, dict), "Spec details are not dict"

    def test_store_hardware_spec_invalid_metadata(self, api_client_mock):
        metadata = {
            api_client_mock.hardware_specifications.ConfigurationMetaNames.NODES: {
                "cpu": {"units": "2"},
                "mem": {"size": "128Gi"},
                "gpu": {"num_gpu": 1},
            }
        }

        hardware_specifications = HwSpec(api_client_mock)

        with pytest.raises(MissingMetaProp):
            hardware_specifications.store(metadata)

    def test_deploy_model_valid(self, api_client_mock, mocker):
        rsp = {
            "metadata": {
                "name": "Deployment name",
                "id": self.deployment_id,
            },
            "entity": {"status": {"state": "ready"}},
        }
        mock_post = mock_data_from_requests("post", mocker, json=rsp, status_code=202)
        mock_get = mock_data_from_requests("get", mocker, json=rsp)

        mocker.patch("time.sleep")

        metadata = {
            "name": "Deployment name",
            "description": "Random description",
            "online": {},
            "hardware_spec": {"name": "Random HwSpec name"},
            "foundation_model": {"max_new_tokens": 4},
        }

        deployments = Deployments(api_client_mock)
        api_client_mock.deployments = deployments

        deployment_details = deployments.create(self.model_asset_id, metadata)

        mock_post.assert_has_calls(
            [
                mocker.call(
                    "{}/v4/deployments",
                    json={
                        "name": "Deployment name",
                        "description": "Random description",
                        "hardware_spec": {"name": "Random HwSpec name"},
                        "online": {
                            "parameters": {"foundation_model": {"max_new_tokens": 4}}
                        },
                        "asset": {"id": self.model_asset_id},
                        "space_id": None,
                    },
                    params={},
                    headers={},
                )
            ]
        )
        mock_get.assert_has_calls(
            [
                mocker.call(
                    "{}/v4/deployments/" + self.deployment_id,
                    {},
                    headers={},
                )
            ]
        )
        assert isinstance(deployment_details, dict), "Details are not dict"

    def test_deploy_model_empty_metadata(self, api_client_mock):
        deployments = Deployments(api_client_mock)

        with pytest.raises(WMLClientError):
            deployments.create(self.model_asset_id)

    def test_deploy_model_invalid_metadata(self, api_client_mock, mocker):
        mock_post = mock_data_from_requests("post", mocker, status_code=404)
        mock_post.text = "Failure deployment reason"

        deployments = Deployments(api_client_mock)

        with pytest.raises(WMLClientError):
            deployments.create(self.model_asset_id)

    def test_model_inference_basic(self, api_client_mock, mocker):
        mock_get, mock_post, deployment_inference = self.setup_model_inference(
            api_client_mock, mocker
        )
        get_calls = [
            mocker.call("{}/v4/deployments/" + self.deployment_id, {'limit': 200}, headers={}),
            mocker.call(
                "{}/ml/v1/foundation_model_specs",
                params={'limit': 200},
                headers={},
            ),
            mocker.call("{}/v4/deployments/" + self.deployment_id, {'limit': 200}, headers={}),
        ]
        post_calls = [
            mocker.call(
                headers={},
                params={"limit": 200},
                url="{}/ml/v1/deployments/{}/text/generation",
                json={"input": "What is 2 + 2?", "parameters": {"max_new_tokens": 4}},
            )
        ]

        response = deployment_inference.generate_text(
            "What is 2 + 2?", params={"max_new_tokens": 4}
        )

        mock_get.assert_has_calls(get_calls)
        mock_post.assert_has_calls(post_calls)
        assert isinstance(response, str), "Generated text is not `str`"
        assert len(response) > 0, "Generated text is empty"

    def test_model_inference_raw_response(self, api_client_mock, mocker):
        mock_get, mock_post, deployment_inference = self.setup_model_inference(
            api_client_mock, mocker
        )

        response = deployment_inference.generate_text(
            "What is 2 + 2?", params={"max_new_tokens": 4}, raw_response=True
        )

        assert isinstance(response, dict), "Generated response is not `dict`"
        assert "results" in response, "No results in response"
