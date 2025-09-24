"""Top-level package for the Medical Summary Builder pipeline."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("medical-summary-builder")
except PackageNotFoundError:  # pragma: no cover - during local development
    __version__ = "0.1.0"

__all__ = ["__version__"]
