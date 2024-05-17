#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watsonx_ai.foundation_models.embeddings.base_embeddings import BaseEmbeddings


class DebugEmbeddings(BaseEmbeddings):
    """Fake Embeddings for testing that return a proportion of English characters in a text."""

    ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self) -> None:
        super().__init__()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_query(text))

        return embeddings

    def embed_query(self, text: str) -> list[float]:
        text = text.lower()  # Convert text to lowercase
        count = {char: 0 for char in self.ALLOWED_CHARS}  # Initialize count for each letter
        total_chars = 0  # Total count of English characters
        for char in text:
            if char.isalpha():  # Check if character is an English alphabet
                count[char] += 1
                total_chars += 1

        # Calculate proportion for each letter
        proportions = [count[char] / max(total_chars, 1) if total_chars > 0 else 0.0 for char in self.ALLOWED_CHARS]
        return proportions

    def to_dict(self) -> dict:
        return super().to_dict()
