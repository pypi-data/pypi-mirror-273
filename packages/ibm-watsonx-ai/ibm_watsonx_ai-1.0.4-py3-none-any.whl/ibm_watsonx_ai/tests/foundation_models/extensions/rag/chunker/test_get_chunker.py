#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai.foundation_models.extensions.rag.chunker import (
    get_chunker,
    LCChunker,
)


class TestGetChunker:
    def test_01_get_langchain_chunker(self):
        chunker_settings = {"method": "recursive"}
        chunker = get_chunker(provider="langchain", settings=chunker_settings)

        assert isinstance(chunker, LCChunker), "chunker should be instance of LCChunker, not {}".format(chunker)

    def test_02_incorrect_chunker_params(self):

        with pytest.raises(ValueError) as e:
            get_chunker("incorrect_provider")

        assert e.match(r"incorrect_provider provider is not supported! Use one of *")
