from __future__ import annotations

from pathlib import Path
from typing import Iterable

from markdownify import markdownify as html_to_markdown


class DocumentConverter:
    """Convert source documents into normalized markdown strings."""

    @staticmethod
    def pdf_page_to_markdown(html_content: str) -> str:
        """Convert extracted HTML from a PDF page into markdown."""

        return html_to_markdown(html_content, heading_style="ATX")

    @staticmethod
    def save_markdown(pages: Iterable[str], output_path: Path | str) -> Path:
        """Persist markdown pages to disk as a single file."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n\n".join(pages), encoding="utf-8")
        return path
