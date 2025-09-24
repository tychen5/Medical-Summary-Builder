from __future__ import annotations

from typing import Iterable

from ..schemas import MedicalSummary, MedicalEvent


class TemplateFiller:
    """Fill summary structures using LLM outputs and custom instructions."""

    def populate_timeline(self, events: Iterable[dict]) -> list[MedicalEvent]:
        return [MedicalEvent(**event) for event in events]

    def apply_custom_tables(self, summary: MedicalSummary, tables: dict[str, list[dict[str, str]]]) -> MedicalSummary:
        summary.custom_tables.update(tables)
        return summary
