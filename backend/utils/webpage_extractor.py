"""
Helpers to extract article text from URLs.
"""

from __future__ import annotations

from typing import Optional

import requests
from bs4 import BeautifulSoup

try:
    from newspaper import Article
except ImportError:  # pragma: no cover - optional
    Article = None  # type: ignore

from .logger import get_logger

logger = get_logger(__name__)


class WebExtractionError(RuntimeError):
    """Raised when article text cannot be fetched."""


def _extract_with_newspaper(url: str) -> Optional[str]:
    if Article is None:
        return None
    article = Article(url)
    article.download()
    article.parse()
    return article.text.strip()


def _extract_with_bs4(url: str) -> Optional[str]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    joined = " ".join(paragraphs).strip()
    return joined or None


def extract_text_from_url(url: str) -> str:
    """Fetch and return cleaned article text."""
    if not url:
        raise ValueError("URL is required.")

    try:
        text = _extract_with_newspaper(url)
        if text:
            return text
    except Exception as exc:  # pragma: no cover - best effort
        logger.warning("newspaper3k extraction failed: %s", exc)

    try:
        text = _extract_with_bs4(url)
        if text:
            return text
    except Exception as exc:
        logger.warning("BeautifulSoup extraction failed: %s", exc)

    raise WebExtractionError("Unable to extract content from URL.")


__all__ = ["extract_text_from_url", "WebExtractionError"]

