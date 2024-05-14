from typing import List
from abc import ABC, abstractmethod

class Embeddings(ABC):
    """Interface for embedding models."""

    @classmethod
    def class_name(cls) -> str:
        return "Embeddings"
    
    @abstractmethod
    def get_query_embedding(self, query: str) -> List[float]:
        """Embed the input query."""

    @abstractmethod
    def get_embedding_from_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed list of texts."""

    @abstractmethod
    def get_documents_embedding(self, documents: List[str]) -> List[List[float]]:
        """Embed list of docs."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.get_embedding_from_texts(texts=texts)