#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------


class TestVectorStoreElasticsearch:
    """
    These tests cover:
    - Elasticsearch support for VectorStore class
    - basic vector store functionalities

    Embedding is done via fake - proportion of english characters in text.
    This is to reduce computational resources to minimum but still provide code readabilty.
    """

    def test_01_basic_add_and_retrieve_documents(self, vectorstore_chroma, ids_to_delete_es):
        docs = [
            {'content': 'aaa', 'metadata': {'url': 'ibm.com'}},
            {'content': 'bbb', 'metadata': {'url': 'ibm_test.com'}},
            {'content': 'ccc'}
        ]

        ids_to_delete_es.extend(vectorstore_chroma.add_documents(docs))

        result = vectorstore_chroma.search('bbb', k=1)

        assert len(result) == 1, "since k=1"

        assert result[0].page_content == docs[1]['content'], "should be 'bbb'"
        assert result[0].metadata['url'] == docs[1]['metadata']['url'], "should be 'ibm_test.com'"

    def test_02_basic_add_and_retrieve_documents_empty(self, vectorstore_chroma):
        result = vectorstore_chroma.search('text', k=1)

        assert len(result) == 0

    def test_03_basic_add_and_delete_documents(self, vectorstore_chroma):
        docs = [
            {'content': 'aaa', 'metadata': {'url': 'ibm.com'}},
            {'content': 'bbb', 'metadata': {'url': 'ibm_test.com'}},
            {'content': 'ccc'}
        ]

        ids = vectorstore_chroma.add_documents(docs)
        result = vectorstore_chroma.search('aaa', k=5)

        assert len(result) == 3, "k=5 but 3 were added"

        vectorstore_chroma.delete(ids)

        result = vectorstore_chroma.search('search query', k=3)

        assert len(result) == 0, "should be 0 because deleted"
