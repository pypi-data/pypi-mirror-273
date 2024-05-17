#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import pytest

from ibm_watsonx_ai.foundation_models.utils.utils import get_embedding_model_specs


from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.wml_client_error import (
    UnexpectedType,
    NoWMLCredentialsProvided,
    WMLClientError,
)

from ibm_watsonx_ai.tests.unit.conftest import mock_data_from_requests


@pytest.mark.unittest
class TestEmbeddings:

    model_name = "ibm/slate-125m-english-rtrvr"
    project_id = "7e8b59ca-2610-4a29-9d90-dc02583ed5f7"
    embed_params = {"truncate_input_tokens": 3}
    get_embedding_model_specs_rsp = {
        "resources": [{"model_id": "ibm/slate-125m-english-rtrvr"}]
    }
    inputs = ["What is a generative ai?", "What is a loan and how does it works?"]

    @staticmethod
    def setup_embeddings(
        api_client_mock,
        mocker,
        project_id=project_id,
        model_id=model_name,
        params=None,
        without_cred=False,
        cpd_version=5.0,
    ):
        api_client_mock.default_project_id = project_id
        api_client_mock.CPD_version = cpd_version
        if without_cred:
            api_client_mock.credentials = None
        response = {
            "results": [
                {"embedding": [-0.053358648, -0.009175377, -0.025022397]},
                {"embedding": [-0.025761532, -0.005709378, -0.021448452]},
            ]
        }
        mock_post = mock_data_from_requests("post", mocker, json=response)
        mock_get = mock_data_from_requests("get", mocker, json=response)

        embeddings = Embeddings(
            model_id=model_id, api_client=api_client_mock, params=params
        )
        return mock_get, mock_post, embeddings

    def test_get_embedding_model_spec(self, api_client_mock, mocker):
        mock_get = mock_data_from_requests(
            "get", mocker, json=self.get_embedding_model_specs_rsp
        )

        model_specs = get_embedding_model_specs(url=api_client_mock.credentials.url)

        mock_get.assert_called_once_with(
            "credentials_url/ml/v1/foundation_model_specs",
            params={"version": "2023-09-30", "filters": "function_embedding"},
            headers={"X-WML-User-Client": "PythonClient"},
        )

        assert "resources" in model_specs, "Specs do not contain `resources` field"

    def test_init_embeddings_without_credentials(self, api_client_mock, mocker):
        with pytest.raises(NoWMLCredentialsProvided) as e:
            self.setup_embeddings(api_client_mock, mocker, without_cred=True)

        assert (
            e.value.error_msg == 'No "WML credentials" provided.'
        ), "Wrong error message"

    def test_init_embeddings_with_incorrect_cpd_version(self, api_client_mock, mocker):
        with pytest.raises(WMLClientError) as e:
            self.setup_embeddings(api_client_mock, mocker, cpd_version=4.8)

        assert (
            e.value.error_msg == "Operation is unsupported for this release."
        ), "Wrong error message"

    def test_generate_embeddings(self, api_client_mock, mocker):
        mock_get, mock_post, embeddings = self.setup_embeddings(api_client_mock, mocker)
        response = embeddings.generate(inputs=self.inputs)

        assert isinstance(response, dict), "Generated response is not `dict`"
        assert "results" in response, "No results in response"

    def test_generate_embeddings_with_params(self, api_client_mock, mocker):
        mock_get, mock_post, embeddings = self.setup_embeddings(
            api_client_mock, mocker, params=self.embed_params
        )
        response = embeddings.generate(inputs=self.inputs)

        assert isinstance(response, dict), "Generated response is not `dict`"
        assert "results" in response, "No results in response"

    def test_generate_embeddings_invalid_inputs(self, api_client_mock, mocker):
        mock_get, mock_post, embeddings = self.setup_embeddings(api_client_mock, mocker)
        with pytest.raises(UnexpectedType):
            embeddings.generate(inputs=self.inputs[0])

    def test_embed_documents(self, api_client_mock, mocker):
        mock_get, mock_post, embeddings = self.setup_embeddings(api_client_mock, mocker)
        response = embeddings.embed_documents(texts=self.inputs)
        assert isinstance(response, list), "Generated response is not `list`"
        for sublist in response:
            assert isinstance(sublist, list), "Sublist is not `list`"
            for element in sublist:
                assert isinstance(
                    element, (int, float)
                ), "Element is not an `int` or `float`"

    def test_embed_query(self, api_client_mock, mocker):
        mock_get, mock_post, embeddings = self.setup_embeddings(api_client_mock, mocker)
        response = embeddings.embed_query(text=self.inputs[0])
        assert isinstance(response, list), "Generated response is not `list`"
        for element in response:
            assert isinstance(
                element, (int, float)
            ), "Element is not an `int` or `float`"

    def test_to_dict(self, api_client_mock, mocker):
        mock_get, mock_post, embeddings = self.setup_embeddings(api_client_mock, mocker)
        response = embeddings.to_dict()
        assert response["model_id"] == self.model_name
        assert response["project_id"] == self.project_id
