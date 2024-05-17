#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import pytest
from ibm_watsonx_ai.wml_client_error import WMLClientError

from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models.utils import get_embedding_model_specs

from ibm_watsonx_ai.tests.utils.utils import get_wml_credentials

credentials = get_wml_credentials()
project_id = credentials.__dict__.get("project_id")
client = APIClient(credentials, project_id=project_id)
available_models = [
    el.get("model_id")
    for el in get_embedding_model_specs(credentials.url).get("resources")
]


class TestFoundationModels:
    """
    This tests covers:
    - Embeddings generate with and without params
    - Embeddings embed_documents (texts)
    - Embeddings embed_query
    - Serialisation: to_dict and from_dict methods
    """

    def test_01_get_model_specs_without_model_id(self):
        res = client.foundation_models.get_model_specs()
        print(res)
        assert "resources" in res
        assert len(res["resources"]) > 0

    def test_02_get_model_specs_with_model_id(self):
        res = client.foundation_models.get_model_specs("ibm/granite-13b-instruct-v2")
        print(res)
        assert res is not None
        assert res.get("model_id") == "ibm/granite-13b-instruct-v2"

    def test_03_get_model_specs_with_model_id_as_model_type(self):
        res = client.foundation_models.get_model_specs(ModelTypes.GRANITE_13B_INSTRUCT_V2)
        print(res)
        assert res is not None
        assert res.get("model_id") == "ibm/granite-13b-instruct-v2"

    def test_04_get_model_specs_with_non_existing_model_id(self):
        res = client.foundation_models.get_model_specs("non_existing")
        print(res)
        assert res is None

    def test_05_get_model_specs_with_limit(self):
        res = client.foundation_models.get_model_specs(limit=2)
        print(res)
        assert res is not None
        assert len(res["resources"]) == 2

    def test_06_get_model_specs_with_invalid_limit(self):
        try:
            client.foundation_models.get_model_specs(limit=-1)
            assert False
        except WMLClientError:
            pass

    @pytest.mark.skipif(client.CLOUD_PLATFORM_SPACES, reason="Not available on cloud")
    def test_07_get_custom_model_specs_without_model_id(self):
        res = client.foundation_models.get_custom_model_specs()
        print(res)
        assert "resources" in res
        assert len(res["resources"]) > 0

    @pytest.mark.skipif(client.CLOUD_PLATFORM_SPACES, reason="Not available on cloud")
    def test_08_get_custom_model_specs_with_model_id(self):
        res = client.foundation_models.get_custom_model_specs("EleutherAI/gpt-j-6b")
        print(res)
        assert res is not None
        assert res.get("model_id") == "EleutherAI/gpt-j-6b"

    @pytest.mark.skipif(client.CLOUD_PLATFORM_SPACES, reason="Not available on cloud")
    def test_09_get_custom_model_specs_with_non_existing_model_id(self):
        res = client.foundation_models.get_custom_model_specs("non_existing")
        print(res)
        assert res is None

    def test_10_get_embeddings_model_specs(self):
        res = client.foundation_models.get_embeddings_model_specs()
        print(res)
        assert "resources" in res
        assert len(res["resources"]) > 0

    def test_11_get_embeddings_model_specs_with_model_id(self):
        res = client.foundation_models.get_embeddings_model_specs(
            "ibm/slate-125m-english-rtrvr"
        )
        print(res)
        assert res is not None
        assert res.get("model_id") == "ibm/slate-125m-english-rtrvr"

    def test_12_get_model_specs_with_prompt_tuning_support(self):
        res = client.foundation_models.get_model_specs_with_prompt_tuning_support()
        print(res)
        assert "resources" in res
        assert len(res["resources"]) > 0

    def test_13_get_model_specs_with_prompt_tuning_support_with_model_id(self):
        res = client.foundation_models.get_model_specs_with_prompt_tuning_support(
            "google/flan-t5-xl"
        )
        print(res)
        assert res is not None
        assert res.get("model_id") == "google/flan-t5-xl"

    def test_14_get_model_lifecycle(self):
        res = client.foundation_models.get_model_lifecycle("ibm/granite-13b-instruct-v2")
        print(res)
        assert isinstance(res, list)
        assert len(res) > 0
        assert res[0].get("id") is not None

    def test_15_get_model_lifecycle_with_non_existing_model_id(self):
        res = client.foundation_models.get_model_lifecycle("non_existing")
        print(res)
        assert res is None
