#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai.foundation_models.extensions.rag import RAGPattern
from ibm_watsonx_ai.foundation_models.extensions.rag.pattern.pattern import DEFAULT_RAG_PARAMS
from ibm_watsonx_ai.wml_client_error import InvalidMultipleArguments, InvalidValue, MissingValue, ValidationError


class TestRAGPattern:
    """
    These tests cover:
    - RAGPattern initialization with various parameter configurations
    - local querying both provided and default functions
    - deploying and deleting RAGPattern
    """

    DUMMY_STR_VALUE = 'value'
    DUMMY_INT_VALUE = 47
    DEFAULT_RAG_PARAMS = {
        'param_1': DUMMY_STR_VALUE,
        'param_2': DUMMY_INT_VALUE,
    }
    DUMMY_SCORE_PAYLOAD = {
        'input_data': [
            {
                'values': 'question'
            }
        ]
    }

    def create_python_function(self):
        def dummy_deployable_function(custom_arg=self.DUMMY_STR_VALUE, params=None):
            def score(payload):
                return payload
            return score
        return dummy_deployable_function

    def test_01_client_and_credentials_missing(self, rag_client):
        with pytest.raises(InvalidMultipleArguments):
            RAGPattern(
                space_id=rag_client.default_space_id
            )

    def test_02_python_function_not_provided_chain_missing(self, rag_client):
        with pytest.raises(MissingValue):
            RAGPattern(
                space_id=rag_client.default_space_id,
                api_client=rag_client,
            )

    def test_03_python_function_provided(self, rag_client):
        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            python_function=self.create_python_function()
        )

        assert pattern.python_function is not None, 'should be function `dummy_deployable_function`'
        assert pattern.python_function.__defaults__[0] == self.DUMMY_STR_VALUE, 'should match the value of `custom_arg`'
        assert pattern.python_function.__defaults__[1] is not None, '`params` parameter should contain credentials, space_id and rag_params'

        assert pattern.vector_store is None, 'should be None as no vector store provided'
        assert pattern.prompt_id is None, 'should be None as no prompt_id provided'
        assert pattern.model is None, 'should be None as no model provided'

    def test_03a_python_function_provided_auto_store(self, rag_client):
        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            python_function=self.create_python_function(),
            auto_store=True
        )

        assert pattern.python_function is not None, 'should be function `dummy_deployable_function`'
        assert pattern.function_id in pattern._client.repository.list_functions().get('ID').to_list(), 'stored function id should be visible in repository'
        assert 'dummy_deployable_function' in pattern._client.repository.list_functions().get('NAME').to_list(), 'stored function name should be visible in repository'

        assert pattern.vector_store is None, 'should be None as no vector store provided'
        assert pattern.prompt_id is None, 'should be None as no prompt_id provided'
        assert pattern.model is None, 'should be None as no model provided'

        pattern._client.repository.delete(pattern.function_id)

    def test_04_params_not_provided(self, rag_client):
        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            python_function=self.create_python_function()
        )

        assert pattern.rag_params == DEFAULT_RAG_PARAMS, f'should be {DEFAULT_RAG_PARAMS} as no rag_params were provided'

    def test_05_params_provided_update(self, rag_client):
        passed_params = {
            'param_1': 'passed_value',
        }
        expected_params = DEFAULT_RAG_PARAMS
        expected_params.update(passed_params)

        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            python_function=self.create_python_function(),
            rag_params=passed_params
        )

        assert pattern.rag_params == expected_params, 'DEFAULT_RAG_PARAMS should be overwritten by passed_params'

    def test_06_chain_provided(self, rag_client, vectorstore, prompt_template, model):
        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            vector_store=vectorstore,
            prompt_id=prompt_template.prompt_id,
            model=model
        )

        assert pattern.python_function is not None, 'should be default function'
        assert pattern.function_id is None, 'should be None as function not yet stored'

        assert pattern.vector_store == vectorstore, 'should not be None as vectorstore provided'
        assert pattern.prompt_id == prompt_template.prompt_id, 'should not be None as prompt_id provided'
        assert pattern.model == model, 'should not be None as model provided'

    def test_07a_chain_provided_with_prompt_text(self, rag_client, vectorstore, model):
        prompt_text = 'dummy prompt with {question} and {reference_documents} placeholders'

        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            vector_store=vectorstore,
            model=model,
            prompt_text=prompt_text
        )

        assert pattern.python_function is not None, 'should be default function'
        assert pattern.function_id is None, 'should be None as function not yet stored'

        assert pattern.vector_store == vectorstore, 'should not be None as vectorstore provided'
        assert pattern.prompt_id is None, 'should be None as prompt_id not provided'
        assert pattern.prompt_text is prompt_text, f'should be: {prompt_text} as prompt_text string provider via kwargs'
        assert pattern.model == model, 'should not be None as model provided'

    def test_07b_chain_provided_with_invalid_prompt_text(self, rag_client, vectorstore, model):
        invalid_prompt_text = 'dummy prompt with {question} and missing docs placeholder'

        with pytest.raises(ValidationError):
            RAGPattern(
                space_id=rag_client.default_space_id,
                api_client=rag_client,
                vector_store=vectorstore,
                model=model,
                prompt_text=invalid_prompt_text
            )

    def test_08_invalid_keyword_argument_provided(self, rag_client):
        with pytest.raises(InvalidValue):
            RAGPattern(
                space_id=rag_client.default_space_id,
                api_client=rag_client,
                python_function=self.create_python_function(),
                invalid_kwarg='invalid'
            )

    def test_11_query_local_chain_provided(self, rag_client, vectorstore, prompt_template, model, ids_to_delete_es):
        docs = [
            {'content': 'IBM was founded on June 16, 1911.', 'metadata': {'url': 'ibm_test.com'}},
            {'content': "Watson's favourite slogan was 'THINK'."}
        ]
        ids_to_delete_es.extend(vectorstore.add_documents(docs))

        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            vector_store=vectorstore,
            prompt_id=prompt_template.prompt_id,
            model=model,
            rag_params={'num_documents_retrieved': 1}
        )

        questions = [
            "When was IBM founded?",
            "What was Watson's favourite slogan?"
        ]
        payload = {
            rag_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                'values': questions
            }]
        }
        response = pattern.query(payload)
        response_values = response['predictions'][0]['values']

        assert len(response_values[0][0]) > 0, 'should contain generated text answer'
        assert response_values[0][1][0]['page_content'] == docs[0]['content'], "first answer's content should match first doc's content"
        assert response_values[0][1][0]['metadata'] == docs[0]['metadata'], "first answer's metadata should match first doc's metadata"

        assert len(response_values[1][0]) > 0, 'should contain generated text answer'
        assert response_values[1][1][0]['page_content'] == docs[1]['content'], "second answer's content should match second doc's content"

    def test_12_query_local_python_function_provided(self, rag_client):
        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            python_function=self.create_python_function()
        )

        response = pattern.query(self.DUMMY_SCORE_PAYLOAD)

        assert response == self.DUMMY_SCORE_PAYLOAD, 'should return the payload as defined in `dummy_deployable_function`'

    @pytest.mark.timeout(5 * 60)
    def test_13_deploy_and_delete_python_function_provided(self, rag_client):
        pattern = RAGPattern(
            space_id=rag_client.default_space_id,
            api_client=rag_client,
            python_function=self.create_python_function()
        )

        custom_function_name = 'custom_function_name'

        pattern.deploy(name='test-rag-pattern-deployment',
                       store_params={'name': custom_function_name})

        function_id = pattern.function_id
        deployment_id = pattern.deployment_id

        assert function_id in rag_client.repository.list_functions().get('ID').to_list(), 'stored function id should be visible in repository'
        assert custom_function_name in rag_client.repository.list_functions().get('NAME').to_list(), 'stored function name should be visible in repository'

        assert pattern.deployment_id in rag_client.deployments.list().get('ID').to_list(), 'deployment id should be visible in repository'

        pattern.delete()

        assert pattern.function_id is None, 'function_id should be cleared after deletion'
        assert function_id not in rag_client.repository.list_functions().get('ID').to_list(), 'function should be deleted from repository'

        assert pattern.deployment_id is None, 'deployment_id should be cleared after deletion'
        assert deployment_id not in rag_client.deployments.list().get('ID').to_list(), 'deployment should be deleted from space'
