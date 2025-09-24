from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from langchain_core.documents import Document


@dataclass
class MetadataRecord:
    claimant_name: str | None = None
    ssn: str | None = None
    dob: str | None = None
    aod: str | None = None
    dli: str | None = None
    education: str | None = None
    alleged_impairments: list[str] | None = None


class MetadataRouter:
    """Accumulate structured claimant metadata using LLM extraction."""

    def __init__(self, llm) -> None:
        self.llm = llm

    def extract(self, documents: Iterable[Document]) -> MetadataRecord:
        # Placeholder for future LLM chain integration
        raise NotImplementedError
