#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import pytest

from ibm_watsonx_ai.foundation_models.prompt_tuner import PromptTuner
from ibm_watsonx_ai.foundation_models.utils import PromptTuningParams
from ibm_watsonx_ai.wml_client_error import WMLClientError, UnexpectedType
from ibm_watsonx_ai.utils.autoai.errors import ContainerTypeNotSupported

from ibm_watsonx_ai.tests.unit.conftest import (
    mock_get_details,
    mock_s3_connection,
)


@pytest.mark.unittest
class TestPromptTuner:
    """
    These tests cover:
    - constructor
    - method run
    - method get_model_id
    - method get_params
    - method cancel_run
    """

    msg = "Firstly schedule a prompt tuning by using the tune() method."

    @pytest.fixture(scope="function", name="prompt_tuner")
    def fixture_prompt_tuner(self, api_client_mock):
        prompt_tuner = PromptTuner(name="random_name", task_id="random_task_id")
        prompt_tuner.id = "random_training_id"
        prompt_tuner._client = api_client_mock
        return prompt_tuner

    def test_init_params(self, prompt_tuner):
        assert prompt_tuner.name == "random_name", "Invalid name"
        assert prompt_tuner.description == "Prompt tuning with SDK", "Invalid desc"
        assert prompt_tuner.auto_update_model is True, "Invalid auto_update_model"
        assert not prompt_tuner.group_by_name, "Invalid group_by_name"
        assert isinstance(
            prompt_tuner.prompt_tuning_params, PromptTuningParams
        ), "Type of prompt_tuning_params is not `PromptTuningParams`"
        assert prompt_tuner.prompt_tuning_params.base_model == {
            "model_id": None
        }, "Invalid base_model"

    def test_run_valid(self, mocker, prompt_tuner):
        training_data_reference = mock_s3_connection(mocker)
        details_mocked = mock_get_details(prompt_tuner._client)
        prompt_tuner._client.training.get_id.return_value = "changed_id"

        res = prompt_tuner.run([training_data_reference])

        assert prompt_tuner.id == "changed_id"
        assert res == details_mocked

    def test_run_no_list_provided(self, mocker, prompt_tuner):
        training_data_reference = mock_s3_connection(mocker)
        mock_get_details(prompt_tuner._client)
        error_msg = "Unexpected type of 'training_data_references'"

        with pytest.raises(UnexpectedType) as e:
            prompt_tuner.run(training_data_reference)

        assert error_msg in e.value.error_msg, f"Invalid error msg: {e.value.error_msg}"

    def test_run_invalid_data_conn_type(self, mocker, prompt_tuner):
        training_data_reference = mock_s3_connection(mocker)
        # Container is not supported on CPD
        prompt_tuner._client.ICP_PLATFORM_SPACES = True

        with pytest.raises(ContainerTypeNotSupported):
            prompt_tuner.run([training_data_reference])

    def test_get_model_id_valid(self, prompt_tuner):
        mock_get_details(prompt_tuner._client, model_id="random_model_id")

        model_id = prompt_tuner.get_model_id()

        assert model_id == "random_model_id"

    def test_get_model_id_no_auto_update(self, prompt_tuner):
        mock_get_details(prompt_tuner._client, auto_update_model="")

        with pytest.raises(WMLClientError):
            prompt_tuner.get_model_id()

    def test_get_params_valid(self, prompt_tuner):
        params = prompt_tuner.get_params()

        assert params == {
            "auto_update_model": True,
            "base_model": {"model_id": None},
            "description": "Prompt tuning with SDK",
            "group_by_name": None,
            "name": "random_name",
            "task_id": "random_task_id",
        }, "Invalid params"

    def test_get_params_change_model(self, prompt_tuner):
        prompt_tuner.prompt_tuning_params.base_model = "sample model"

        params = prompt_tuner.get_params()

        assert params["base_model"] == "sample model", "Invalid model"

    def test_get_params_change_name(self, prompt_tuner):
        prompt_tuner.name = "new name"

        params = prompt_tuner.get_params()

        assert params["name"] == "new name", "Invalid name param"

    def test_get_params_change_group_by_name(self, prompt_tuner):
        prompt_tuner.group_by_name = True

        params = prompt_tuner.get_params()

        assert params["group_by_name"] is True, "Invalid group_by_name param"

    def test_get_run_status_valid(self, prompt_tuner):
        prompt_tuner._client.training.get_status.return_value = {"state": "completed"}

        status = prompt_tuner.get_run_status()

        assert status == "completed", "Invalid run status"

    def test_get_run_status_no_id(self, prompt_tuner):
        prompt_tuner.id = None

        with pytest.raises(WMLClientError) as e:
            prompt_tuner.get_run_status()

        assert self.msg in e.value.error_msg, f"Invalid error msg: {e.value.error_msg}"

    def test_cancel_run_valid(self, prompt_tuner):
        prompt_tuner.cancel_run()

        prompt_tuner._client.training.cancel.assert_called_once_with(
            hard_delete=False, training_id=prompt_tuner.id
        )

    def test_cancel_run_no_id(self, prompt_tuner):
        prompt_tuner.id = None

        with pytest.raises(WMLClientError) as e:
            prompt_tuner.cancel_run()

        assert self.msg in e.value.error_msg, f"Invalid error msg: {e.value.error_msg}"
