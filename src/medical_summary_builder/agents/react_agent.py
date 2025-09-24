from __future__ import annotations

from typing import Sequence

from langchain.prompts import ChatPromptTemplate
from langgraph.prebuilt import chat_agent_executor

from ..llm import LLMClientFactory
from ..vectorstore import VectorIndexManager


def create_react_agent(tools: Sequence, *, system_prompt: str | None = None):
    """Instantiate a ReAct-style agent for iterative extraction."""

    llm = LLMClientFactory.create(temperature=0.1)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt or "You are an expert medical analyst."),
            ("human", "{input}"),
        ]
    )

    return chat_agent_executor.create_react_agent(
        llm=llm,
        prompt=prompt,
        tools=tools,
        state_modifier=None,
    )
