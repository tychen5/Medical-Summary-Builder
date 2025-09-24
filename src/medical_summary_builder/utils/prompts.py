from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


@dataclass
class PromptTemplate:
    name: str
    description: str
    content: str


class PromptLibrary:
    """Load pre-authored prompt templates from disk."""

    def __init__(self, directory: Path | str) -> None:
        self.directory = Path(directory)

    def load_all(self) -> dict[str, PromptTemplate]:
        prompts: dict[str, PromptTemplate] = {}
        if not self.directory.exists():
            return prompts

        for path in self.directory.glob("*.md"):
            prompts[path.stem] = PromptTemplate(
                name=path.stem,
                description=path.stem.replace("_", " ").title(),
                content=path.read_text(encoding="utf-8"),
            )
        return prompts

    def load(self, name: str) -> PromptTemplate:
        path = self.directory / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt template missing: {path}")
        return PromptTemplate(
            name=name,
            description=name.replace("_", " ").title(),
            content=path.read_text(encoding="utf-8"),
        )

    def to_mapping(self) -> Mapping[str, str]:
        return {template.name: template.content for template in self.load_all().values()}
