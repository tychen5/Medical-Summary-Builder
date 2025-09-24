from __future__ import annotations

import logging
from typing import List, Optional

import openai
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import PrivateAttr
from langchain_openai import OpenAIEmbeddings

from ..config import settings

logger = logging.getLogger(__name__)


class NebiusOpenAIEmbeddings(Embeddings):
    """
    Custom embeddings that prioritize Nebius and fall back to OpenAI.
    Truncates embeddings to a specified dimension.
    """

    _nebius_client: Optional[openai.OpenAI] = PrivateAttr(default=None)
    _openai_client: Optional[OpenAIEmbeddings] = PrivateAttr(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if settings.nebius_api_key:
            self._nebius_client = openai.OpenAI(
                base_url=settings.nebius_api_base_url,
                api_key=settings.nebius_api_key,
            )
        if settings.openai_api_key:
            self._openai_client = OpenAIEmbeddings(
                model=settings.openai_embedding_model,
                api_key=settings.openai_api_key,
                dimensions=settings.embedding_dimensions,
            )

    def _get_nebius_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self._nebius_client:
            raise RuntimeError("Nebius client not configured. NEBIUS_API_KEY missing?")

        response = self._nebius_client.embeddings.create(model=settings.nebius_embedding_model, input=texts)
        return [item.embedding for item in response.data]

    def _truncate_embeddings(self, embeddings: List[List[float]]) -> List[List[float]]:
        return [emb[: settings.embedding_dimensions] for emb in embeddings]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self._nebius_client:
            try:
                logger.info("Attempting to use Nebius for embeddings.")
                embeddings = self._get_nebius_embeddings(texts)
                return self._truncate_embeddings(embeddings)
            except Exception as e:
                logger.warning(f"Nebius embedding failed: {e}. Falling back to OpenAI.")

        if self._openai_client:
            logger.info("Using OpenAI for embeddings.")
            return self._openai_client.embed_documents(texts)

        raise ValueError("No embedding client configured. Set NEBIUS_API_KEY or OPENAI_API_KEY.")

    def embed_query(self, text: str) -> List[float]:
        if self._nebius_client:
            try:
                logger.info("Attempting to use Nebius for query embedding.")
                embeddings = self._get_nebius_embeddings([text])
                return self._truncate_embeddings(embeddings)[0]
            except Exception as e:
                logger.warning(f"Nebius query embedding failed: {e}. Falling back to OpenAI.")

        if self._openai_client:
            logger.info("Using OpenAI for query embedding.")
            return self._openai_client.embed_query(text)

        raise ValueError("No embedding client configured. Set NEBIUS_API_KEY or OPENAI_API_KEY.")


class EmbeddingFactory:
    """Factory for embedding models used for vector storage."""

    @staticmethod
    def create(*, provider: Optional[str] = None, model_name: Optional[str] = None) -> Embeddings:
        # provider and model_name are ignored to support the new Nebius-first with OpenAI fallback logic.
        return NebiusOpenAIEmbeddings()
