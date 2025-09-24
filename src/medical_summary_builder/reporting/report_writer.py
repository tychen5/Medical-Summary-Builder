from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument

from ..schemas import MedicalSummary
from ..utils import ensure_directory


class ReportWriter:
    """Render structured medical summaries into DOCX and markdown outputs."""

    def __init__(self, output_dir: Path | str) -> None:
        self.output_dir = ensure_directory(output_dir)

    def write_markdown(self, summary: MedicalSummary, filename: str = "medical_summary.md") -> Path:
        """Persist the medical summary to markdown for auditing."""

        path = Path(self.output_dir) / filename
        content_lines: list[str] = [
            "# Medical Summary",
            "",
            "## Claimant Profile",
        ]
        for field_name, value in summary.profile.model_dump().items():
            content_lines.append(f"- **{field_name.replace('_', ' ').title()}**: {value or 'N/A'}")
        content_lines.append("")
        content_lines.append("## Timeline of Medical Events")
        for event in summary.events:
            content_lines.append(
                f"- {event.date or 'N/A'} | {event.provider or 'N/A'} | {event.reason or 'N/A'} | {event.reference or 'N/A'}"
            )
        path.write_text("\n".join(content_lines), encoding="utf-8")
        return path

    def write_docx(self, summary: MedicalSummary, template_path: Path | str | None = None) -> Path:
        """Persist the medical summary to a DOCX template."""

        document = DocxDocument(template_path) if template_path else DocxDocument()
        # Placeholder: actual implementation will populate runs/tables matching template style
        document.add_heading("Medical Summary", level=1)
        document.add_heading("Claimant Profile", level=2)
        for field_name, value in summary.profile.model_dump().items():
            document.add_paragraph(f"{field_name.replace('_', ' ').title()}: {value or 'N/A'}")

        document.add_heading("Timeline of Medical Events", level=2)
        table = document.add_table(rows=1, cols=4)
        table.style = "Light List"
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Date"
        hdr_cells[1].text = "Provider"
        hdr_cells[2].text = "Reason"
        hdr_cells[3].text = "Reference"

        for event in summary.events:
            row_cells = table.add_row().cells
            row_cells[0].text = str(event.date or "")
            row_cells[1].text = event.provider or ""
            row_cells[2].text = event.reason or ""
            row_cells[3].text = event.reference or ""

        output_path = Path(self.output_dir) / "medical_summary.docx"
        document.save(str(output_path))
        return output_path
