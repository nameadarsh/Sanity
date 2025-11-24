"""
PDF extraction helpers.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Optional, Sequence

import pdfplumber
from PyPDF2 import PdfReader

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover - optional dependency
    fitz = None  # type: ignore

from .logger import get_logger

logger = get_logger(__name__)


class PDFExtractionError(RuntimeError):
    """Raised when text cannot be extracted from a PDF."""


def _validate_source(
    file_path: Optional[Path],
    file_bytes: Optional[bytes],
) -> None:
    if not file_path and not file_bytes:
        raise ValueError("Either file_path or file_bytes must be provided.")
    if file_path and not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")


def _extract_with_pdfplumber(pdf_stream) -> Sequence[str]:
    with pdfplumber.open(pdf_stream) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def _extract_with_pypdf2(pdf_stream) -> Sequence[str]:
    reader = PdfReader(pdf_stream)
    return [page.extract_text() or "" for page in reader.pages]


def _extract_with_pymupdf(file_path: Path) -> Sequence[str]:
    if fitz is None:
        raise PDFExtractionError("PyMuPDF is not installed.")
    doc = fitz.open(file_path)
    return [page.get_text() for page in doc]


def _merge_chunks(chunks: Sequence[str]) -> str:
    return "\n".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())


def extract_text_from_pdf(
    file_path: Optional[str | Path] = None,
    file_bytes: Optional[bytes] = None,
) -> str:
    """
    Extract text from a PDF using multiple fallbacks.

    Args:
        file_path: Path to the PDF file.
        file_bytes: Raw bytes (e.g., uploaded file).
    """

    path_obj = Path(file_path) if file_path else None
    _validate_source(path_obj, file_bytes)

    # Priority 1: pdfplumber
    streams = []
    if file_bytes:
        streams.append(io.BytesIO(file_bytes))
    if path_obj:
        streams.append(path_obj)

    for stream in streams:
        try:
            chunks = _extract_with_pdfplumber(stream)
            text = _merge_chunks(chunks)
            if text:
                return text
        except Exception as exc:  # pragma: no cover - best effort fallback
            logger.warning("pdfplumber extraction failed: %s", exc)

    # Priority 2: PyPDF2
    for stream in streams:
        try:
            chunks = _extract_with_pypdf2(stream)
            text = _merge_chunks(chunks)
            if text:
                return text
        except Exception as exc:
            logger.warning("PyPDF2 extraction failed: %s", exc)

    # Priority 3: PyMuPDF (file path only)
    if path_obj:
        try:
            chunks = _extract_with_pymupdf(path_obj)
            text = _merge_chunks(chunks)
            if text:
                return text
        except Exception as exc:
            logger.warning("PyMuPDF extraction failed: %s", exc)

    raise PDFExtractionError("Unable to extract text from PDF.")


__all__ = ["extract_text_from_pdf", "PDFExtractionError"]

