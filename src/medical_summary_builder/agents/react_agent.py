from __future__ import annotations

from typing import Any, Sequence, Type

from langgraph.prebuilt import chat_agent_executor
from pydantic import BaseModel

from ..llm import LLMClientFactory
from ..vectorstore import VectorIndexManager


def create_react_agent(
    tools: Sequence,
    *,
    system_prompt: str | None = None,
    response_format: Type[BaseModel] | None = None,
):
    """Instantiate a ReAct-style agent for iterative extraction."""

    llm = LLMClientFactory.create(temperature=0.1,provider="openai")

    return chat_agent_executor.create_react_agent(
        model=llm,
        prompt=system_prompt or "You are an expert medical analyst.",
        tools=tools,
        response_format=response_format,
    )
