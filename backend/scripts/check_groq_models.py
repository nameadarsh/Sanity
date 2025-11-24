"""
Script to check available Groq models and test which one works.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODELS_API_URL = "https://api.groq.com/openai/v1/models"


def get_available_models():
    """Get list of available models from Groq API."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(MODELS_API_URL, headers=headers, timeout=10)
        if response.ok:
            data = response.json()
            models = [model["id"] for model in data.get("data", [])]
            return models
        else:
            print(f"Error fetching models: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def test_model(model_name: str) -> tuple[bool, str]:
    """Test if a model works with a simple request."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "Say 'test' if you can read this."}
        ],
        "temperature": 0.0,
        "max_tokens": 10,
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=15)
        if response.ok:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return True, f"Success: {content}"
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get("error", {}).get("message", response.text)
            return False, f"Error {response.status_code}: {error_msg}"
    except Exception as e:
        return False, f"Exception: {str(e)}"


def main():
    """Main function to check and test models."""
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not found in environment variables!")
        print("Please set it in your .env file.")
        return
    
    print("=" * 60)
    print("Groq Model Availability Checker")
    print("=" * 60)
    print(f"\nAPI Key: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-4:]}")
    print()
    
    # Get available models
    print("Fetching available models from Groq API...")
    models = get_available_models()
    
    if not models:
        print("\n[WARN] Could not fetch models list. Testing common models instead...")
        models = [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "llama-3.1-405b-reasoning",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama-3.2-90b-text-preview",
        ]
    else:
        print(f"[OK] Found {len(models)} available models")
    
    print("\n" + "=" * 60)
    print("Testing Models")
    print("=" * 60)
    print()
    
    working_models = []
    failed_models = []
    
    # Test each model
    for model in models:
        print(f"Testing: {model}")
        success, message = test_model(model)
        
        if success:
            print(f"  [OK] WORKING: {message}")
            working_models.append(model)
        else:
            print(f"  [FAIL] FAILED: {message}")
            failed_models.append((model, message))
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    
    if working_models:
        print("[OK] WORKING MODELS:")
        for model in working_models:
            print(f"  - {model}")
        print()
        print(f"[RECOMMENDED] {working_models[0]}")
        print()
        print("To use this model, update backend/utils/llm_handler.py:")
        print(f'  DEFAULT_MODEL = "{working_models[0]}"')
    else:
        print("[ERROR] NO WORKING MODELS FOUND!")
        print("\nPlease check:")
        print("  1. Your GROQ_API_KEY is correct")
        print("  2. You have API credits/quota")
        print("  3. Your internet connection")
    
    if failed_models:
        print()
        print("[FAILED] MODELS:")
        for model, reason in failed_models:
            print(f"  - {model}: {reason}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()

