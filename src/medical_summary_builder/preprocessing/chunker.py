from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class ChunkedDocument:
    text: str
    metadata: dict[str, object]


class DocumentChunker:
    """Chunk raw documents into overlapping windows for embedding."""

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )

    def split(self, documents: Iterable[Document]) -> list[ChunkedDocument]:
        chunks: list[ChunkedDocument] = []
        for doc in documents:
            chunk_docs = self.splitter.create_documents([doc.page_content], [doc.metadata])
            for chunk_doc in chunk_docs:
                chunks.append(
                    ChunkedDocument(
                        text=chunk_doc.page_content,
                        metadata=chunk_doc.metadata,
                    )
                )
        return chunks
