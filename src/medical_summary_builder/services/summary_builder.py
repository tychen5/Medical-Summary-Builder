from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..pipelines import MedicalSummaryPipeline
from ..reporting import ReportWriter
from ..schemas import MedicalSummary
from ..config import settings


class SummaryBuilderService:
    """Facade that orchestrates ingestion, extraction, and report generation."""

    def __init__(self, pipeline: MedicalSummaryPipeline | None = None) -> None:
        self.pipeline = pipeline or MedicalSummaryPipeline()

    def build_summary(
        self,
        *,
        pdf_path: Path | str,
        template_path: Path | str,
        custom_instruction: Optional[str] = None,
        emit_reports: bool = True,
    ) -> MedicalSummary:
        summary = self.pipeline.run(
            pdf_path=pdf_path,
            template_path=template_path,
            custom_instruction=custom_instruction,
        )

        if emit_reports:
            writer = ReportWriter(settings.reports_dir)
            writer.write_markdown(summary)
            writer.write_docx(summary, template_path=template_path)

        return summary
