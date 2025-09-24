from __future__ import annotations

from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_nebius import NebiusEmbeddings
from langchain_openai import OpenAIEmbeddings

from ..config import settings


class EmbeddingFactory:
    """Factory for embedding models used for vector storage."""

    @staticmethod
    def create(*, provider: Optional[str] = None, model_name: Optional[str] = None) -> Embeddings:
        selected_provider = provider or ("nebius" if settings.nebius_api_key else "openai")

        if selected_provider == "nebius":
            if not settings.nebius_api_key:
                raise ValueError("NEBIUS_API_KEY is required for Nebius embeddings")
            return NebiusEmbeddings(
                model=model_name or settings.embedding_model_name,
                nebius_api_key=settings.nebius_api_key,
            )

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")
        return OpenAIEmbeddings(
            model=model_name or "text-embedding-3-large",
            api_key=settings.openai_api_key,
        )
