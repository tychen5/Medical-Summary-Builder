from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration for the Medical Summary Builder pipeline."""

    # API keys and model configuration
    nebius_api_key: Optional[str] = Field(default=None, env="NEBIUS_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")

    pinecone_api_key: Optional[str] = Field(default=None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(default=None, env="PINECONE_ENVIRONMENT")
    pinecone_index: str = Field(default="medical-summary-index")

    model_name: str = Field(default="NLP-qa-large")
    embedding_model_name: str = Field(default="text-embedding-3-large")

    # Chunking parameters
    chunk_size: int = Field(default=1500)
    chunk_overlap: int = Field(default=200)

    # Directories
    cache_dir: Path = Field(default=Path(".cache/"))
    data_dir: Path = Field(default=Path("Data/"))
    templates_dir: Path = Field(default=Path("Data/templates/"))
    prompts_dir: Path = Field(default=Path("prompts/"))
    outputs_dir: Path = Field(default=Path("outputs/"))
    reports_dir: Path = Field(default=Path("outputs/reports/"))
    diagnostics_dir: Path = Field(default=Path("outputs/diagnostics/"))

    # Runtime flags
    enable_telemetry: bool = Field(default=False)
    dry_run: bool = Field(default=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # Automatically read from environment where available
