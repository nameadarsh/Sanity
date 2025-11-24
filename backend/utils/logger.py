"""
Logging utilities for the Sanity backend.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "sanity_backend.log"
DEV_PROGRESS_FILE = BASE_DIR / "dev_progress.txt"


def ensure_parent(path: Path) -> None:
    """Ensure the parent directory for the given path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Create or retrieve a configured logger."""
    logger = logging.getLogger(name or "sanity")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    ensure_parent(LOG_FILE)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.propagate = False
    return logger


def update_progress_log(message: str) -> None:
    """Append a timestamped progress update."""
    ensure_parent(DEV_PROGRESS_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with DEV_PROGRESS_FILE.open("a", encoding="utf-8") as fp:
        fp.write(f"[{timestamp}] {message}\n")


def log_and_raise(logger: logging.Logger, exc: Exception, message: str) -> None:
    """Utility to log an error before raising the exception."""
    logger.error("%s | %s", message, exc, exc_info=True)
    raise exc


__all__ = ["get_logger", "update_progress_log", "log_and_raise"]

