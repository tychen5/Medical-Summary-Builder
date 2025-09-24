from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument


class TemplateLoader:
    """Load the baseline template metadata from a DOCX file."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def load(self) -> DocxDocument:
        if not self.path.exists():
            raise FileNotFoundError(f"Template not found: {self.path}")
        return DocxDocument(str(self.path))
