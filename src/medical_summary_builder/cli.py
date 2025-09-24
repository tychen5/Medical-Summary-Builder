from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional

import typer

from .config import settings
from .services import SummaryBuilderService


def build(
    pdf_path: Path = typer.Option(..., exists=True, readable=True, help="Path to the source medical PDF."),
    template_path: Path = typer.Option(..., exists=True, readable=True, help="Path to the medical summary template (DOCX)."),
    custom_instruction_file: Optional[Path] = typer.Option(
        None, exists=True, readable=True, help="Optional path to a markdown file with custom table instructions."
    ),
    skip_reports: bool = typer.Option(False, help="If set, do not emit markdown/DOCX reports."),
) -> None:
    """Build a medical summary from the provided case file."""

    service = SummaryBuilderService()
    instruction_text: Optional[str] = None

    if custom_instruction_file:
        instruction_text = custom_instruction_file.read_text(encoding="utf-8")

    summary = service.build_summary(
        pdf_path=pdf_path,
        template_path=template_path,
        custom_instruction=instruction_text,
        emit_reports=not skip_reports,
    )
    typer.echo("Summary generation completed.")
    if settings.reports_dir.exists() and not skip_reports:
        typer.echo(f"Reports saved to: {settings.reports_dir}")


def main() -> None:
    # Backward compatibility: allow calling `python -m medical_summary_builder.cli build ...`
    # by stripping the legacy subcommand name before Typer parses arguments.
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        sys.argv.pop(1)

    typer.run(build)


if __name__ == "__main__":
    main()
