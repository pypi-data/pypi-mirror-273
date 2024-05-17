#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai.tests.foundation_models.extensions.rag.test_classes.debug_embeddings import DebugEmbeddings
from ibm_watsonx_ai.foundation_models.extensions.rag.vector_stores.vector_store_connector import VectorStoreConnector
from ibm_watsonx_ai.tests.utils import get_db_credentials


class TestVectorStoreConnector():
    """
    These tests cover:
    - initializing different vector stores using different available methods,
    """

    def test_01_initialize_chroma(self):
        VectorStoreConnector({'embeddings': DebugEmbeddings()}).get_chroma()

    def test_02_initialize_elasticsearch_no_params(self):
        with pytest.raises(ValueError):
            VectorStoreConnector({}).get_elasticsearch()

    def test_03_initialize_elasticsearch_missing_password(self):
        with pytest.raises(ValueError):
            VectorStoreConnector({'url': 'example.com', 'username': 'user123'}).get_elasticsearch()

    def test_04_initialize_elasticsearch_missing_api_key(self):
        with pytest.raises(ValueError):
            VectorStoreConnector({'use_anonymous_access': 'true', 'es_cloud_id': '1234'}).get_elasticsearch()

    def test_05_initialize_elasticsearch_cloud_ok(self):
        params = get_db_credentials('elasticsearch')
        assert VectorStoreConnector({
            'use_anonymous_access': 'true',
            'url': params['url'],
            'api_key': params['apikey'],
            'index_name': 'test_index',
            'es_params': {'verify_certs': False}
        }).get_elasticsearch()

    def test_06_initialize_elasticsearch_connection_ok(self):
        params = get_db_credentials('elasticsearch')
        assert VectorStoreConnector({
            'use_anonymous_access': 'true',
            'username': params['username'],
            'password': params['password'],
            'url': params['url'],
            'index_name': 'test_index',
            'es_params': {'verify_certs': False}
        }).get_elasticsearch()

    def test_07_unexpected_parameter(self):
        with pytest.raises(TypeError):
            params = get_db_credentials('elasticsearch')
            assert VectorStoreConnector({
                'use_anonymous_access': 'true',
                'username': params['username'],
                'password': params['password'],
                'url': params['url'],
                'index_name': 'test_index',
                'es_params': {'verify_certs': False},
                'this_parameter_will_never_be_here': 'this_value_is_for_testing'
            }).get_elasticsearch()

    def test_08_missing_password(self):
        with pytest.raises(ValueError):
            params = get_db_credentials('elasticsearch')
            assert VectorStoreConnector({
                'use_anonymous_access': 'true',
                'username': params['username'],
                'url': params['url'],
                'index_name': 'test_index',
                'es_params': {'verify_certs': False},
            }).get_elasticsearch()

    def test_09_ssl_certificate_invalid(self):
        with pytest.raises(ValueError, match="SSL certificate"):
            params = get_db_credentials('elasticsearch')
            assert VectorStoreConnector({
                'use_anonymous_access': 'true',
                'username': params['username'],
                'password': params['password'],
                'url': params['url'],
                'index_name': 'test_index',
                'es_params': {'verify_certs': False},
                'ssl_certificate': '1234iaminvalidcertificate1234'
            }).get_elasticsearch()

    def test_10_no_embeddings_if_required(self):
        with pytest.raises(ValueError, match="Embedding"):
            assert VectorStoreConnector({}).get_chroma()  # Chroma expects at least embeddings
