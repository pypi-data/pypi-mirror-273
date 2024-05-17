#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------


import pytest

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models.extensions.rag import VectorStore
from ibm_watsonx_ai.tests.foundation_models.extensions.rag.test_classes.debug_embeddings import DebugEmbeddings
from ibm_watsonx_ai.tests.utils import get_wml_credentials, get_db_credentials

from langchain_community.embeddings import DeterministicFakeEmbedding


@pytest.fixture(scope="class", name='rag_client')
def fixture_setup_rag_client():
    credentials = get_wml_credentials()
    project_id = credentials.project_id
    client = APIClient(credentials, project_id=project_id)
    return client


@pytest.fixture(scope="class", name='vectorstore_elasticsearch')
def fixture_setup_vectorstore_elasticsearch(rag_client):

    # Prepare elasticsearch
    es_credentials = get_db_credentials('elasticsearch')

    # Create connection
    elasticsearch_data_source_type_id = rag_client.connections.get_datasource_type_id_by_name('elasticsearch')
    details = rag_client.connections.create(
        {
            rag_client.connections.ConfigurationMetaNames.NAME: "ES Connection",
            rag_client.connections.ConfigurationMetaNames.DESCRIPTION: "connection description",
            rag_client.connections.ConfigurationMetaNames.DATASOURCE_TYPE: elasticsearch_data_source_type_id,
            rag_client.connections.ConfigurationMetaNames.PROPERTIES:
            {
                "url": es_credentials['url'],
                "username": es_credentials['username'],
                "password": es_credentials['password'],
                "use_anonymous_access": 'false',
                'ssl_certificate': es_credentials['base64_cert']
            }
        }
    )

    connection_id = rag_client.connections.get_id(details)

    # Create VectorStore (that uses elasticsearch) for testing
    vector_store = VectorStore(rag_client, connection_id=connection_id,
                               params={'index_name': es_credentials['index_name']})
    vector_store.set_embeddings(DebugEmbeddings())

    yield vector_store

    rag_client.connections.delete(connection_id)


@pytest.fixture(scope="class", name='vectorstore_milvus')
def fixture_setup_vectorstore_milvus(rag_client):

    # Prepare milvus
    milvus_credentials = get_db_credentials('milvus')

    # Create connection
    milvus_data_source_type_id = rag_client.connections.get_datasource_type_uid_by_name('milvus')
    details = rag_client.connections.create(
        {
            rag_client.connections.ConfigurationMetaNames.NAME: "Milvus Connection",
            rag_client.connections.ConfigurationMetaNames.DESCRIPTION: "connection description",
            rag_client.connections.ConfigurationMetaNames.DATASOURCE_TYPE: milvus_data_source_type_id,
            rag_client.connections.ConfigurationMetaNames.PROPERTIES:
            {
                "host": milvus_credentials['host'],
                "port": milvus_credentials['port'],
                "username": milvus_credentials['username'],
                "password": milvus_credentials['password'],
            }
        }
    )

    connection_id = rag_client.connections.get_uid(details)

    # Create VectorStore (that uses milvus) for testing
    vector_store = VectorStore(
        rag_client,
        connection_id=connection_id,
        params={
            'collection_name': milvus_credentials['collection_name'],
            'connection_args': {'secure': True},
            'consistency_level': 'Strong'  # To make Milvus more ACID compliant
        },
        embeddings=DebugEmbeddings(),
    )

    yield vector_store

    rag_client.connections.delete(connection_id)


@pytest.fixture(scope="function", name='vectorstore_chroma')
def fixture_setup_vectorstore_chroma(rag_client):
    # Create VectorStore (that uses chroma) for testing
    vector_store = VectorStore(
        rag_client,
        data_source_type='chroma',
        embeddings=DebugEmbeddings(),
    )

    yield vector_store

    vector_store._vector_store._langchain_vector_store.delete_collection()


@pytest.fixture(scope='function', name='ids_to_delete_es')
def fixture_ids_to_delete_es(vectorstore_elasticsearch):
    ids = []
    yield ids
    vectorstore_elasticsearch.delete(ids)


@pytest.fixture(scope='function', name='ids_to_delete_milvus')
def fixture_ids_to_delete_milvus(vectorstore_milvus):
    ids = []
    yield ids
    vectorstore_milvus.delete(ids)


@pytest.fixture(scope='function', name='ids_to_delete_chroma')
def fixture_ids_to_delete_chroma(vectorstore_chroma):
    ids = []
    yield ids
    vectorstore_chroma.delete(ids)
