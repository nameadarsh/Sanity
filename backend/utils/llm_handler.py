"""
Groq API helper utilities.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from .logger import get_logger
from .prompts import format_prompt

logger = get_logger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"  # Updated: verified working model from check_groq_models.py


class GroqAPIError(RuntimeError):
    """Raised when the Groq API returns an error."""


@dataclass
class GroqResponse:
    prediction: str
    reasoning: str
    raw: Dict[str, Any]


class GroqClient:
    """Lightweight client for the Groq chat completions endpoint."""

    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing. Please set it in the environment.")
        self.model = model

    def _request(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "messages": messages, "temperature": temperature}
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        if not response.ok:
            logger.error("Groq API error %s: %s", response.status_code, response.text)
            raise GroqAPIError(f"Groq API error: {response.text}")
        return response.json()

    def call_llm(self, prompt_template: List[Dict[str, str]], **kwargs) -> str:
        """
        Call LLM with a formatted prompt template.
        
        Args:
            prompt_template: List of message dicts with {{placeholder}} syntax
            **kwargs: Values to substitute into placeholders
            
        Returns:
            LLM response text
        """
        messages = format_prompt(prompt_template, **kwargs)
        result = self._request(messages, temperature=0.0)
        return result["choices"][0]["message"]["content"]

    def verify_article(self, article_text: str) -> GroqResponse:
        """Run the verification prompt (low confidence auto-verification)."""
        from .prompts import PROMPT_LOW_CONFIDENCE_VERIFY
        
        content = self.call_llm(PROMPT_LOW_CONFIDENCE_VERIFY, article_text=article_text)
        prediction, reasoning = self._parse_verification_response(content)
        
        # Get raw response for compatibility
        messages = format_prompt(PROMPT_LOW_CONFIDENCE_VERIFY, article_text=article_text)
        raw_result = self._request(messages)
        
        return GroqResponse(prediction=prediction, reasoning=reasoning, raw=raw_result)

    def answer_question(
        self,
        question: str,
        article_text: Optional[str] = None,
        model_prediction: Optional[str] = None,
        verification_summary: Optional[str] = None,
    ) -> str:
        """
        Answer a question - either direct question or follow-up about an article.
        
        Args:
            question: User's question
            article_text: Article content (if follow-up question)
            model_prediction: Model's prediction (if follow-up question)
            verification_summary: Verification output (if follow-up question)
            
        Returns:
            LLM response
        """
        from .prompts import PROMPT_DIRECT_QUESTION, PROMPT_FOLLOWUP_NEWS
        
        # Determine if this is a follow-up question or direct question
        if article_text:
            # Follow-up question about a news article
            return self.call_llm(
                PROMPT_FOLLOWUP_NEWS,
                article_text=article_text,
                model_prediction=model_prediction or "Unknown",
                verification_summary=verification_summary or "Not available",
                user_question=question,
            )
        else:
            # Direct question (general query)
            return self.call_llm(PROMPT_DIRECT_QUESTION, user_question=question)

    @staticmethod
    def _parse_verification_response(content: str) -> tuple[str, str]:
        """
        Parse LLM verification response to extract prediction and reasoning.
        Normalizes prediction to exactly 'Real' or 'Fake'.
        """
        prediction, reasoning = "Unknown", content
        
        # Try to find prediction and reasoning in the response
        lines = content.splitlines()
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            # Look for "Prediction: Real/Fake" pattern
            if "prediction" in line_lower and ":" in line:
                pred_text = line.split(":", 1)[-1].strip()
                # Normalize to "Real" or "Fake"
                if "real" in pred_text.lower():
                    prediction = "Real"
                elif "fake" in pred_text.lower():
                    prediction = "Fake"
            
            # Look for "Reasoning:" pattern
            if "reasoning" in line_lower and ":" in line:
                # Get reasoning from this line onwards
                reasoning_parts = [line.split(":", 1)[-1].strip()]
                # Collect remaining lines as reasoning
                for remaining_line in lines[i + 1:]:
                    if remaining_line.strip() and not remaining_line.lower().startswith("prediction"):
                        reasoning_parts.append(remaining_line.strip())
                reasoning = " ".join(reasoning_parts).strip()
                break
        
        # Fallback: if no explicit reasoning found, use the full content
        if reasoning == content or not reasoning:
            # Try to extract reasoning by removing prediction line
            reasoning_lines = []
            for line in lines:
                if not line.lower().strip().startswith("prediction"):
                    reasoning_lines.append(line.strip())
            reasoning = " ".join(reasoning_lines).strip() or content
        
        # Final validation: ensure prediction is Real or Fake
        if prediction not in ["Real", "Fake"]:
            # Try to infer from content
            content_lower = content.lower()
            if "real" in content_lower and "fake" not in content_lower[:content_lower.find("real") + 10]:
                prediction = "Real"
            elif "fake" in content_lower:
                prediction = "Fake"
            else:
                logger.warning("Could not parse prediction from LLM response, defaulting to 'Unknown'")
                prediction = "Unknown"
        
        return prediction, reasoning


__all__ = ["GroqClient", "GroqResponse", "GroqAPIError", "call_llm"]


def call_llm(prompt_template: List[Dict[str, str]], **kwargs) -> str:
    """
    Convenience function to call LLM with a prompt template.
    
    Args:
        prompt_template: List of message dicts with {{placeholder}} syntax
        **kwargs: Values to substitute into placeholders
        
    Returns:
        LLM response text
    """
    client = GroqClient()
    return client.call_llm(prompt_template, **kwargs)

