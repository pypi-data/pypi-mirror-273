#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai.client import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.extensions.rag import VectorStore
from ibm_watsonx_ai.foundation_models.prompts import PromptTemplateManager, PromptTemplate
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.tests.utils import get_wml_credentials, get_db_credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes


@pytest.fixture(scope="class", name='rag_client')
def fixture_setup_rag_client(space_id):
    credentials = get_wml_credentials()
    client = APIClient(credentials, space_id=space_id)
    return client


@pytest.fixture(scope="class", name='vectorstore')
def fixture_setup_vectorstore_elasticsearch(rag_client):
    es_credentials = get_db_credentials('elasticsearch')
    elasticsearch_data_source_type_id = rag_client.connections.get_datasource_type_id_by_name('elasticsearch')

    details = rag_client.connections.create(
        {
            rag_client.connections.ConfigurationMetaNames.NAME: "ES Connection",
            rag_client.connections.ConfigurationMetaNames.DESCRIPTION: "connection description",
            rag_client.connections.ConfigurationMetaNames.DATASOURCE_TYPE: elasticsearch_data_source_type_id,
            rag_client.connections.ConfigurationMetaNames.PROPERTIES:
            {
                "password": es_credentials['password'],
                "url": es_credentials['url'],
                "username": es_credentials['username'],
                "use_anonymous_access": 'false',
                'ssl_certificate': es_credentials['base64_cert']
            }
        }
    )

    connection_id = rag_client.connections.get_id(details)
    vs_params = {
        'index_name': es_credentials['index_name'] + "_test_sdk_wx_embeddings",
    }
    vector_store = VectorStore(rag_client,
                               connection_id=connection_id,
                               params=vs_params)
    vector_store.set_embeddings(Embeddings(model_id=EmbeddingTypes.IBM_SLATE_30M_ENG, 
                                           api_client=rag_client))
    yield vector_store

    rag_client.connections.delete(connection_id)


@pytest.fixture(scope="class", name='prompt_template')
def fixture_setup_prompt_template(rag_client):
    PROMPT_INSTRUCTION = \
    """
    Use the following pieces of documents to answer the question
    at the end. If you don't know the answer, just say that you
    don't know, don't try to make up an answer. Use three sentences
    maximum. Keep the answer as concise as possible. do not include
    question in your response.Your answers should not include any
    harmful, unethical, racist, sexist, toxic, dangerous, or illegal
    content. Please ensure that your responses are socially unbiased
    and positive in nature.\nPlease provide a concise professional
    response.
    """
    prompt_mgr = PromptTemplateManager(api_client=rag_client)
    prompt_template = PromptTemplate(name="RAG_prompt_template",
                                     model_id=ModelTypes.LLAMA_2_13B_CHAT,
                                     input_variables=["question", "reference_documents"],
                                     instruction=PROMPT_INSTRUCTION,
                                     input_text="{reference_documents}\nQuestion:{question}\nAnswer:")
    stored_prompt_template = prompt_mgr.store_prompt(prompt_template=prompt_template)
    yield stored_prompt_template

    prompt_mgr.unlock(stored_prompt_template.prompt_id)
    prompt_mgr.delete_prompt(stored_prompt_template.prompt_id)


@pytest.fixture(scope="class", name='model')
def fixture_setup_model(rag_client):
    model = ModelInference(
        model_id=ModelTypes.LLAMA_2_13B_CHAT,
        params={
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.MAX_NEW_TOKENS: 200
        },
        api_client=rag_client
    )
    return model


@pytest.fixture(scope='function', name='ids_to_delete_es')
def fixture_ids_to_delete_es(vectorstore):
    ids = []
    yield ids
    vectorstore.delete(ids)
