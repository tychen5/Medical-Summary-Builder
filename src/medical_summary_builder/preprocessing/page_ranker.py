from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from langchain_core.documents import Document


@dataclass
class RankedPage:
    score: float
    document: Document


class PageRelevanceRanker:
    """Rank PDF pages for downstream extraction workflows."""

    def __init__(self, llm, *, window_size: int = 3) -> None:
        self.llm = llm
        self.window_size = window_size

    def rank(self, documents: Sequence[Document], instruction: str) -> list[RankedPage]:
        # Placeholder logic will be replaced with LLM-based scoring
        return [
            RankedPage(score=1.0, document=doc)
            for doc in documents
        ]
