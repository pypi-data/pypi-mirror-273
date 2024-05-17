#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from typing import Sequence, Any
from abc import ABC, abstractmethod

from langchain_core.documents import Document


__all__ = [
    "BaseChunker",
]


class BaseChunker(ABC):
    """
    Class responsible for handling operations of splitting documents
    within the RAG application.
    """

    @abstractmethod
    def split_documents(
        self, documents: Sequence[str | Document]
    ) -> list[str | Document]:
        """
        Split series of documents into smaller parts based on
        the provided chunker settings.

        :param documents: sequence of elements that contain context in the format of text
        :type: Sequence[str | Document]

        :return: list of documents splitter into smaller ones, having less content
        :rtype: list[str | Document]
        """

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Return dict that can be used to recreate instance of the LCChunker."""

    @abstractmethod
    def from_dict(self, d: dict[str, Any]) -> 'BaseChunker':
        """Create instance from the dictionary"""
