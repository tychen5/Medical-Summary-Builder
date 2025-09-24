from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def configure_logging(log_file: Path | None = None, level: int = logging.INFO) -> None:
    """Configure structured logging for the application."""

    log_dir = Path("outputs/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    handlers: dict[str, dict[str, object]] = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": level,
        }
    }

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": str(log_file),
            "level": level,
        }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LOG_FORMAT,
                }
            },
            "handlers": handlers,
            "root": {
                "handlers": list(handlers.keys()),
                "level": level,
            },
        }
    )
