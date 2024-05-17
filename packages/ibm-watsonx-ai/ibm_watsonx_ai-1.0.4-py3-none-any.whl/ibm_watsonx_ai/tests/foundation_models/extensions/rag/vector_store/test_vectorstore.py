#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai.foundation_models.extensions.rag import VectorStore
from ibm_watsonx_ai.foundation_models.extensions.rag.vector_stores.vector_store_connector import VectorStoreDataSourceType
from ibm_watsonx_ai.tests.foundation_models.extensions.rag.test_classes.debug_embeddings import DebugEmbeddings
from ibm_watsonx_ai.wml_client_error import ApiRequestFailure


class TestVectorStore:
    """
    These tests cover:
    - Initializing VectorStore with missing params (before VectorStoreConnector call)
    - Serialization/Deserialization
    """

    def test_01_initialize_vector_store_no_params(self, rag_client):
        with pytest.raises(TypeError):
            VectorStore(client=rag_client)

    def test_02_initialize_vector_store_incorrect_langchain(self, rag_client):
        with pytest.raises(TypeError):
            VectorStore(client=rag_client, langchain_vector_store='some invalid stuff')

    def test_03_initialize_vector_store_incorrect_connection_id(self, rag_client):
        with pytest.raises(ApiRequestFailure):
            VectorStore(client=rag_client, connection_id='1234abc')

    def test_04_initialize_vector_store_no_client_with_connection_id(self):
        with pytest.raises(ValueError):
            VectorStore(connection_id='1234abc')

    def test_05_initialize_vector_store_incorrect_data_source(self):
        with pytest.raises(TypeError):
            VectorStore(data_source_type='undefined_data_source_test')

    def test_06_serialization_deserialization(self):
        vs = VectorStore(data_source_type=VectorStoreDataSourceType.CHROMA, embeddings=DebugEmbeddings())
        data = vs.to_dict()

        assert data == \
            {
                'connection_id': None,
                'data_source_type': 'chroma',
                'params': {},
                'embeddings': {
                    '__class__': 'DebugEmbeddings',
                    '__module__': 'ibm_watsonx_ai.tests.foundation_models.extensions.rag.test_classes.debug_embeddings',
                },
            }

        vs_deserialized = VectorStore.from_dict(None, data)

        assert vs_deserialized._data_source_type == 'chroma', "deserialization 'VectorStoreDataSourceType.CHROMA is 'chroma'"
        assert vs_deserialized._connection_id is None, "should be None, same as default parameter"

        assert isinstance(vs_deserialized._embeddings, DebugEmbeddings), "should of DebugEmbeddings type, same as parameter"
