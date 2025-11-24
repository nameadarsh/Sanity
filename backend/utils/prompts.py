"""
Prompt templates for the three LLM interaction flows.
"""

from __future__ import annotations

from typing import List, Dict


def format_prompt(template: List[Dict[str, str]], **kwargs) -> List[Dict[str, str]]:
    """
    Format a prompt template by replacing placeholders with actual values.
    
    Args:
        template: List of message dicts with {{placeholder}} syntax
        **kwargs: Values to substitute into placeholders
        
    Returns:
        Formatted prompt ready for LLM API
    """
    formatted = []
    for msg in template:
        content = msg["content"]
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        formatted.append({"role": msg["role"], "content": content})
    return formatted


PROMPT_DIRECT_QUESTION = [
    {
        "role": "system",
        "content": (
            "You are an expert AI assistant. The user is asking a general question. "
            "You must answer using strictly correct, verified, up-to-date information. "
            "Always structure the output as clear bullet points. "
            "Never guess or hallucinate. If uncertain, say 'Information not confirmed'."
        ),
    },
    {
        "role": "user",
        "content": (
            "User question:\n{{user_question}}\n\n"
            "Respond only with accurate and fact-checked bullet points."
        ),
    },
]


PROMPT_FOLLOWUP_NEWS = [
    {
        "role": "system",
        "content": (
            "You are assisting the user in understanding a specific news article. "
            "You must use ONLY the provided context. "
            "Do not add new facts outside the article unless they are universally verified and up-to-date. "
            "Always answer clearly, factually, and without speculation."
        ),
    },
    {
        "role": "user",
        "content": (
            "Article Content:\n{{article_text}}\n\n"
            "Original Prediction: {{model_prediction}}\n"
            "Verification Summary (if available): {{verification_summary}}\n\n"
            "User's Follow-Up Question:\n{{user_question}}\n\n"
            "Provide a reliable, context-based answer backed strictly by the content above."
        ),
    },
]


PROMPT_LOW_CONFIDENCE_VERIFY = [
    {
        "role": "system",
        "content": (
            "You are an AI fact-checking model assisting in verifying whether a news "
            "article is real or fake. The local classifier has low confidence. "
            "Your job is to determine Real or Fake and give strictly factual reasoning. "
            "Use only verified, up-to-date, and non-speculative information. "
            "Keep reasoning to 2–3 concise sentences."
        ),
    },
    {
        "role": "user",
        "content": (
            "Article to verify:\n{{article_text}}\n\n"
            "Respond exactly in this format:\n\n"
            "Prediction: Real/Fake\n"
            "Reasoning: <2–3 factual sentences>"
        ),
    },
]


__all__ = [
    "PROMPT_DIRECT_QUESTION",
    "PROMPT_FOLLOWUP_NEWS",
    "PROMPT_LOW_CONFIDENCE_VERIFY",
    "format_prompt",
]

