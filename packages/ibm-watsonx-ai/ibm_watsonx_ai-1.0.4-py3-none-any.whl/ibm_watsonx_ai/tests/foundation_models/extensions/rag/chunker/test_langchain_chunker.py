#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai.foundation_models.extensions.rag.chunker import LCChunker

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
)
from langchain_core.documents import Document


@pytest.fixture(name="documents")
def fixture_documents() -> list[Document]:
    """Create list of documents used during testing."""
    raw_docs = [
        "Article I.\n\nSection 1.\n\t\t\tAll legislative Powers herein granted shall be vested in a Congress of "
        "the United States, which shall consist of a Senate and House of Representatives."
        "\nSection 2.\n\t\t\tThe House of Representatives shall be composed of Members chosen every second Year by "
        "the People ofthe several States, and the Electors in each State shall have the Qualifications requisite for "
        "Electors of the most numerous Branch of the State Legislature."
    ]
    return [Document(page_content=doc) for doc in raw_docs]


class TestLangchainChunker:

    @pytest.mark.parametrize(
        "method, text_splitter",
        [
            ("recursive", RecursiveCharacterTextSplitter),
            ("character", CharacterTextSplitter),
            ("token", TokenTextSplitter),
        ],
    )
    def test_01_get_chunker_with_langchain_text_splitter(self, method, text_splitter):
        chunker = LCChunker(method=method)

        assert isinstance(
            chunker._text_splitter, text_splitter
        ), "chunker's TextSplitter should be {} instead of {}".format(
            text_splitter.__name__, chunker._text_splitter.__class__.__name__
        )

    def test_02_chunker_raises_value_error_on_incorrect_method(self):

        with pytest.raises(ValueError) as e:
            chunker = LCChunker(method="unknown")

        assert e.match(r"Chunker method 'unknown' is not supported. Use one of *")

    def test_03_document_splitting(self, documents):
        chunker = LCChunker(method="recursive", chunk_size=64, chunk_overlap=16)

        split_docs = chunker.split_documents(documents)

        assert (
            len(split_docs) == 11
        ), "Expected split to 11 documents, but got {} instead".format(len(split_docs))
        assert isinstance(
            split_docs[0], Document
        ), "documents should be instances of Document, not {}".format(
            type(split_docs[0])
        )

    def test_04_to_dict(self):
        chunker = LCChunker(method="recursive", chunk_size=64, chunk_overlap=16)

        d = chunker.to_dict()

        expected = {
            "method": "recursive",
            "chunk_size": 64,
            "chunk_overlap": 16,
            "model_name": None,
            "encoding_name": "gpt2",
        }

        assert d == expected, "Instance casted to dict is different than expected"

    def test_05_from_dict(self):
        d = {
            "method": "recursive",
            "chunk_size": 64,
            "chunk_overlap": 16,
            "model_name": None,
            "encoding_name": "gpt2",
        }

        chunker = LCChunker(method="recursive", chunk_size=64, chunk_overlap=16)
        chunker_from_dict = LCChunker.from_dict(d)

        assert (
            chunker == chunker_from_dict
        ), "Recreated chunker from dict is different than the original"
