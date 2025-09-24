from __future__ import annotations

from typing import Iterable

from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from ..config import settings


class VectorIndexManager:
    """Wrap Pinecone index creation and retrieval utilities."""

    def __init__(self, embeddings: Embeddings, index_name: str | None = None) -> None:
        self.embeddings = embeddings
        self.index_name = index_name or settings.pinecone_index

    def upsert(self, documents: Iterable[Document]) -> PineconeVectorStore:
        return PineconeVectorStore.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=self.index_name,
        )

    def as_retriever(self, *, search_kwargs: dict | None = None) -> PineconeVectorStore:
        search_kwargs = search_kwargs or {"k": 8}
        return PineconeVectorStore(
            embedding=self.embeddings,
            index_name=self.index_name,
            search_kwargs=search_kwargs,
        )
