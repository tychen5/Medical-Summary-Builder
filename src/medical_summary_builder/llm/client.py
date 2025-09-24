from __future__ import annotations

from typing import Literal, Optional

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatNebius
from langchain_core.language_models.chat_models import BaseChatModel

from ..config import settings

ModelProvider = Literal["nebius", "openai"]


class LLMClientFactory:
    """Factory for chat completion models used throughout the pipeline."""

    @staticmethod
    def create(
        *,
        provider: ModelProvider | None = None,
        model_name: Optional[str] = None,
        temperature: float = 0.2,
    ) -> BaseChatModel:
        selected_provider: ModelProvider

        if provider is not None:
            selected_provider = provider
        elif settings.nebius_api_key:
            selected_provider = "nebius"
        else:
            selected_provider = "openai"

        if selected_provider == "nebius":
            if not settings.nebius_api_key:
                raise ValueError("NEBIUS_API_KEY is required for Nebius provider")
            return ChatNebius(
                model=model_name or settings.model_name,
                temperature=temperature,
                nebius_api_key=settings.nebius_api_key,
            )

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")

        return ChatOpenAI(
            model=model_name or "gpt-5-nano",
            temperature=temperature,
            api_key=settings.openai_api_key,
        )
