"""
Flask backend for the Sanity real vs fake news project.
"""

from __future__ import annotations

import base64
import os
import uuid
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import torch
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

try:
    from .utils import (
        GroqAPIError,
        GroqClient,
        get_logger,
        update_progress_log,
        extract_text_from_pdf,
        extract_text_from_url,
        clean_text_for_prompt,
    )
except ImportError:  # pragma: no cover - script execution fallback
    import sys

    sys.path.append(str(Path(__file__).resolve().parent))
    from utils import (
        GroqAPIError,
        GroqClient,
        get_logger,
        update_progress_log,
        extract_text_from_pdf,
        extract_text_from_url,
        clean_text_for_prompt,
    )

load_dotenv()

app = Flask(__name__)
CORS(app)
logger = get_logger(__name__)

MODEL_DIR = Path(os.getenv("MODEL_DIR", "backend/model/distilbert"))
FINE_TUNED_MODEL_PATH = Path(os.getenv("FINE_TUNED_MODEL_PATH", "backend/model/sanity_model.bin"))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_tokenizer: DistilBertTokenizerFast | None = None
_model: DistilBertForSequenceClassification | None = None
_groq_client: GroqClient | None = None

# Context storage for follow-up questions
# Key: session_id or article_id, Value: dict with article_text, prediction, verification, etc.
_article_contexts: Dict[str, Dict[str, Any]] = {}


def load_model() -> Tuple[DistilBertTokenizerFast, DistilBertForSequenceClassification]:
    """Load tokenizer/model from disk, downloading if necessary."""
    global _tokenizer, _model
    if _tokenizer and _model:
        return _tokenizer, _model

    try:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        _tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR, local_files_only=True)
        _model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR, local_files_only=True)
        logger.info("Loaded DistilBERT from %s", MODEL_DIR)
    except Exception:
        logger.warning("Local model missing, downloading distilbert-base-uncased.")
        _tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
        _model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
        _tokenizer.save_pretrained(MODEL_DIR)
        _model.save_pretrained(MODEL_DIR)
        update_progress_log("Downloaded base DistilBERT weights.")

    if FINE_TUNED_MODEL_PATH.exists():
        state_dict = torch.load(FINE_TUNED_MODEL_PATH, map_location="cpu")
        missing, unexpected = _model.load_state_dict(state_dict, strict=False)
        if missing or unexpected:
            logger.warning("State dict mismatch. Missing: %s | Unexpected: %s", missing, unexpected)
        logger.info("Loaded fine-tuned weights from %s", FINE_TUNED_MODEL_PATH)

    _model.to(DEVICE)
    _model.eval()
    return _tokenizer, _model


def get_groq_client() -> GroqClient:
    global _groq_client
    if _groq_client:
        return _groq_client
    _groq_client = GroqClient()
    return _groq_client


def resolve_text(payload: Dict[str, Any]) -> str:
    """Derive article text from the incoming payload."""
    input_type = (payload.get("input_type") or "text").lower()
    if input_type == "text":
        text = payload.get("text") or payload.get("content")
        if not text:
            raise ValueError("No text provided.")
        return text
    if input_type == "url":
        url = payload.get("url") or payload.get("content")
        if not url:
            raise ValueError("URL missing for url input type.")
        return extract_text_from_url(url)
    if input_type == "pdf":
        pdf_path = payload.get("pdf_path")
        pdf_b64 = payload.get("pdf_base64")
        if pdf_path:
            return extract_text_from_pdf(file_path=pdf_path)
        if pdf_b64:
            pdf_bytes = base64.b64decode(pdf_b64)
            return extract_text_from_pdf(file_bytes=pdf_bytes)
        raise ValueError("PDF input requires pdf_path or pdf_base64.")
    raise ValueError(f"Unsupported input_type '{input_type}'.")


def run_model_inference(text: str) -> Dict[str, Any]:
    tokenizer, model = load_model()
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt",
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    probs = torch.softmax(logits, dim=-1).cpu().numpy().flatten()
    confidence = float(np.max(probs))
    label_idx = int(np.argmax(probs))
    labels = {0: "Fake", 1: "Real"}
    label = labels.get(label_idx, "Unknown")
    return {
        "label": label,
        "confidence": confidence,
        "needs_verification": confidence < CONFIDENCE_THRESHOLD,
        "probabilities": {"fake": float(probs[0]), "real": float(probs[1])},
    }


@app.route("/health", methods=["GET"])
def health() -> Any:
    try:
        load_model()
        model_status = "ready"
    except Exception as exc:
        logger.error("Health check model load failed: %s", exc)
        model_status = "error"
    return jsonify(
        {
            "status": "ok" if model_status == "ready" else "degraded",
            "model": model_status,
            "device": str(DEVICE),
        }
    )


@app.route("/predict", methods=["POST"])
def predict() -> Any:
    payload = request.get_json(force=True) or {}
    try:
        text = resolve_text(payload)
        inference = run_model_inference(text)
        
        # Auto-verify if confidence is low
        verification_result = None
        if inference["needs_verification"]:
            logger.info("Low confidence detected (%.3f), auto-verifying with LLM", inference["confidence"])
            try:
                client = get_groq_client()
                # Clean text before sending to LLM
                cleaned_text = clean_text_for_prompt(text, max_length=8000)  # Reasonable limit
                verification_result = client.verify_article(cleaned_text)
                logger.info("Auto-verification complete | prediction=%s", verification_result.prediction)
            except Exception as exc:
                logger.warning("Auto-verification failed: %s", exc)
                # Continue without verification
        
        # Generate context ID for follow-up questions
        context_id = payload.get("context_id") or str(uuid.uuid4())
        
        # Store context for follow-up questions
        _article_contexts[context_id] = {
            "article_text": text,
            "model_prediction": inference["label"],
            "model_confidence": inference["confidence"],
            "verification": verification_result.reasoning if verification_result else None,
            "verification_prediction": verification_result.prediction if verification_result else None,
        }
        
        response = {
            "article_text": text,
            "context_id": context_id,  # Return context_id so frontend can use it for follow-ups
            **inference,
        }
        
        # Add verification result if auto-verified
        if verification_result:
            response["auto_verification"] = {
                "prediction": verification_result.prediction,
                "reasoning": verification_result.reasoning,
            }
        
        logger.info("Prediction complete | label=%s confidence=%.3f", inference["label"], inference["confidence"])
        return jsonify(response)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # pragma: no cover - general safeguard
        logger.exception("Prediction failed.")
        return jsonify({"error": "Prediction failed", "details": str(exc)}), 500


@app.route("/verify", methods=["POST"])
def verify() -> Any:
    payload = request.get_json(force=True) or {}
    article_text = payload.get("article_text")
    if not article_text:
        return jsonify({"error": "article_text is required"}), 400
    try:
        client = get_groq_client()
        result = client.verify_article(article_text)
        return jsonify(
            {
                "prediction": result.prediction,
                "reasoning": result.reasoning,
                "raw": result.raw,
            }
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 503
    except GroqAPIError as exc:
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        logger.exception("Verification failed.")
        return jsonify({"error": "Verification failed", "details": str(exc)}), 500


@app.route("/ask", methods=["POST"])
def ask() -> Any:
    """
    Handle both direct questions and follow-up questions about articles.
    
    For follow-up questions:
        - Provide context_id from a previous /predict call
        - OR provide article_text, model_prediction, verification_summary
    
    For direct questions:
        - Just provide question (no context_id or article fields)
    """
    payload = request.get_json(force=True) or {}
    question = payload.get("question")
    if not question:
        return jsonify({"error": "question is required"}), 400
    
    try:
        client = get_groq_client()
        context_id = payload.get("context_id")
        
        # Check if this is a follow-up question about an article
        if context_id and context_id in _article_contexts:
            # Follow-up question about a news article
            context = _article_contexts[context_id]
            # Clean text before sending to LLM
            cleaned_text = clean_text_for_prompt(context["article_text"], max_length=8000)
            answer = client.answer_question(
                question=question,
                article_text=cleaned_text,
                model_prediction=context["model_prediction"],
                verification_summary=context["verification"] or "Not available",
            )
            logger.info("Answered follow-up question for context_id=%s", context_id)
        elif payload.get("article_text"):
            # Follow-up question with explicit context
            cleaned_text = clean_text_for_prompt(payload.get("article_text", ""), max_length=8000)
            answer = client.answer_question(
                question=question,
                article_text=cleaned_text,
                model_prediction=payload.get("model_prediction", "Unknown"),
                verification_summary=payload.get("verification_summary", "Not available"),
            )
            logger.info("Answered follow-up question with explicit context")
        else:
            # Direct question (general query)
            answer = client.answer_question(question=question)
            logger.info("Answered direct question")
        
        return jsonify({"answer": answer})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 503
    except GroqAPIError as exc:
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        logger.exception("Q&A failed.")
        return jsonify({"error": "Q&A failed", "details": str(exc)}), 500


@app.route("/log", methods=["POST"])
def log_progress() -> Any:
    payload = request.get_json(force=True) or {}
    message = payload.get("message")
    if not message:
        return jsonify({"error": "message is required"}), 400
    update_progress_log(message)
    return jsonify({"status": "logged"})


if __name__ == "__main__":
    update_progress_log("Starting Flask backend server.")
    app.run(host="0.0.0.0", port=5000, debug=True)

