from __future__ import annotations

from pathlib import Path
from typing import Iterable

from langchain_core.documents import Document
from pypdf import PdfReader


class PDFMedicalLoader:
    """Load medical PDF source files into LangChain `Document` objects."""

    def __init__(self, path: Path | str, *, include_empty: bool = False) -> None:
        self.path = Path(path)
        self.include_empty = include_empty

    def load(self) -> list[Document]:
        """Return a list of `Document` chunks — one per PDF page."""

        if not self.path.exists():
            raise FileNotFoundError(f"PDF source not found: {self.path}")

        reader = PdfReader(str(self.path))
        total_pages = len(reader.pages)
        documents: list[Document] = []

        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip() or self.include_empty:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(self.path),
                            "page_number": page_index,
                            "page_label": f"{page_index}/{total_pages}",
                        },
                    )
                )

        return documents

    def iter_text(self) -> Iterable[str]:
        """Yield the raw text of each page for lightweight processing."""

        for document in self.load():
            yield document.page_content
