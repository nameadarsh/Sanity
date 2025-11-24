"""
Automatically update the Groq model in llm_handler.py based on available models.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LLM_HANDLER_PATH = Path(__file__).resolve().parent.parent / "utils" / "llm_handler.py"

# Preferred models in order of preference
PREFERRED_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "groq/compound",
]


def test_model(model_name: str) -> bool:
    """Test if a model works."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": "test"}],
        "temperature": 0.0,
        "max_tokens": 5,
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=10)
        return response.ok
    except Exception:
        return False


def find_working_model() -> str | None:
    """Find the first working model from preferred list."""
    print("Testing preferred models...")
    for model in PREFERRED_MODELS:
        print(f"  Testing: {model}...", end=" ")
        if test_model(model):
            print("OK")
            return model
        print("FAILED")
    return None


def update_llm_handler(model_name: str) -> bool:
    """Update DEFAULT_MODEL in llm_handler.py."""
    try:
        content = LLM_HANDLER_PATH.read_text(encoding="utf-8")
        
        # Find and replace DEFAULT_MODEL line
        pattern = r'DEFAULT_MODEL\s*=\s*"[^"]*"'
        replacement = f'DEFAULT_MODEL = "{model_name}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            LLM_HANDLER_PATH.write_text(new_content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"Error updating file: {e}")
        return False


def main():
    """Main function."""
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not found!")
        return
    
    print("=" * 60)
    print("Auto-Update Groq Model")
    print("=" * 60)
    print()
    
    working_model = find_working_model()
    
    if not working_model:
        print("\n[ERROR] No working model found from preferred list!")
        print("Please run check_groq_models.py to see all available models.")
        return
    
    print(f"\n[OK] Found working model: {working_model}")
    print(f"Updating {LLM_HANDLER_PATH}...")
    
    if update_llm_handler(working_model):
        print(f"[SUCCESS] Updated DEFAULT_MODEL to: {working_model}")
        print("\nPlease restart the backend server for changes to take effect.")
    else:
        print("[INFO] Model already set or update failed.")


if __name__ == "__main__":
    main()

