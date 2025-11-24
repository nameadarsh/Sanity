"""
Text cleaning utilities for preparing content for LLM prompts.
"""

from __future__ import annotations

import re
from typing import Optional


def clean_text_for_prompt(text: str, max_length: Optional[int] = None) -> str:
    """
    Clean text before including in LLM prompts.
    
    Removes excessive whitespace, normalizes line breaks, and optionally truncates.
    
    Args:
        text: Raw text to clean
        max_length: Optional maximum character length (truncates if longer)
        
    Returns:
        Cleaned text ready for prompt inclusion
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    
    # Normalize line breaks
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        # Truncate at word boundary if possible
        truncated = text[:max_length]
        last_space = truncated.rfind(" ")
        if last_space > max_length * 0.8:  # Only use word boundary if it's not too early
            text = truncated[:last_space] + "..."
        else:
            text = truncated + "..."
    
    return text


__all__ = ["clean_text_for_prompt"]

