from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration for the Medical Summary Builder pipeline."""

    # API keys and model configuration
    nebius_api_key: Optional[str] = Field(default=None, env="NEBIUS_API_KEY")
    nebius_api_base_url: str = Field(default="https://api.studio.nebius.com/v1/", env="NEBIUS_API_BASE_URL")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")

    pinecone_api_key: Optional[str] = Field(default=None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(default=None, env="PINECONE_ENVIRONMENT")
    pinecone_index: str = Field(default="medical-summary-index")

    model_name: str = Field(default="Qwen/Qwen3-235B-A22B-Thinking-2507")
    nebius_embedding_model: str = Field(default="Qwen/Qwen3-Embedding-8B")
    openai_embedding_model: str = Field(default="text-embedding-3-small")
    embedding_dimensions: int = Field(default=1536)

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
        extra = "ignore"


settings = Settings()  # Automatically read from environment where available
