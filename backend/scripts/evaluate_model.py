"""
Evaluate the fine-tuned model and generate confusion matrix.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

try:
    from ..utils import get_logger, update_progress_log
except ImportError:  # pragma: no cover - script mode
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from utils import get_logger, update_progress_log

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "model" / "distilbert"
FINE_TUNED_MODEL_PATH = BASE_DIR / "model" / "sanity_model.bin"

logger = get_logger(__name__)


def load_model_and_tokenizer():
    """Load fine-tuned model and tokenizer."""
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    
    if FINE_TUNED_MODEL_PATH.exists():
        state_dict = torch.load(FINE_TUNED_MODEL_PATH, map_location="cpu")
        model.load_state_dict(state_dict, strict=False)
        logger.info("Loaded fine-tuned weights from %s", FINE_TUNED_MODEL_PATH)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return tokenizer, model, device


def predict_batch(texts: list[str], tokenizer, model, device, batch_size: int = 32):
    """Run inference on a batch of texts."""
    all_predictions = []
    all_probs = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        inputs = tokenizer(
            batch_texts,
            padding="max_length",
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
            predictions = np.argmax(probs, axis=-1)
        
        all_predictions.extend(predictions.tolist())
        all_probs.extend(probs.tolist())
    
    return np.array(all_predictions), np.array(all_probs)


def evaluate(test_path: Path, output_dir: Path | None = None):
    """Evaluate model on test set and generate confusion matrix."""
    logger.info("Loading test dataset from %s", test_path)
    test_df = pd.read_csv(test_path)
    
    if "text" not in test_df.columns or "label" not in test_df.columns:
        raise ValueError("Test CSV must have 'text' and 'label' columns.")
    
    texts = test_df["text"].fillna("").astype(str).tolist()
    true_labels = test_df["label"].astype(int).tolist()
    
    logger.info("Loaded %d test samples", len(texts))
    
    tokenizer, model, device = load_model_and_tokenizer()
    logger.info("Running predictions...")
    
    predictions, probabilities = predict_batch(texts, tokenizer, model, device)
    
    # Calculate metrics
    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, average="binary", zero_division=0
    )
    
    # Confusion matrix
    cm = confusion_matrix(true_labels, predictions)
    
    # Classification report
    report = classification_report(
        true_labels,
        predictions,
        target_names=["Fake", "Real"],
        output_dict=True,
    )
    
    # Print results
    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"\nTest Set Size: {len(texts)}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    print("\n" + "-" * 60)
    print("CONFUSION MATRIX")
    print("-" * 60)
    print("\n                Predicted")
    print("              Fake    Real")
    print(f"Actual Fake   {cm[0][0]:5d}   {cm[0][1]:5d}")
    print(f"       Real   {cm[1][0]:5d}   {cm[1][1]:5d}")
    
    print("\n" + "-" * 60)
    print("DETAILED CLASSIFICATION REPORT")
    print("-" * 60)
    print(f"\nFake News:")
    print(f"  Precision: {report['0']['precision']:.4f}")
    print(f"  Recall:    {report['0']['recall']:.4f}")
    print(f"  F1-Score:  {report['0']['f1-score']:.4f}")
    print(f"  Support:   {report['0']['support']}")
    
    print(f"\nReal News:")
    print(f"  Precision: {report['1']['precision']:.4f}")
    print(f"  Recall:    {report['1']['recall']:.4f}")
    print(f"  F1-Score:  {report['1']['f1-score']:.4f}")
    print(f"  Support:   {report['1']['support']}")
    
    print(f"\nMacro Average:")
    print(f"  Precision: {report['macro avg']['precision']:.4f}")
    print(f"  Recall:    {report['macro avg']['recall']:.4f}")
    print(f"  F1-Score:  {report['macro avg']['f1-score']:.4f}")
    
    print(f"\nWeighted Average:")
    print(f"  Precision: {report['weighted avg']['precision']:.4f}")
    print(f"  Recall:    {report['weighted avg']['recall']:.4f}")
    print(f"  F1-Score:  {report['weighted avg']['f1-score']:.4f}")
    
    # Save confusion matrix to file if output_dir specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save confusion matrix as CSV
        cm_df = pd.DataFrame(
            cm,
            index=["Actual Fake", "Actual Real"],
            columns=["Predicted Fake", "Predicted Real"],
        )
        cm_path = output_dir / "confusion_matrix.csv"
        cm_df.to_csv(cm_path)
        logger.info("Saved confusion matrix to %s", cm_path)
        
        # Save full report
        report_path = output_dir / "evaluation_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("MODEL EVALUATION REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Test Set Size: {len(texts)}\n")
            f.write(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)\n")
            f.write(f"Precision: {precision:.4f}\n")
            f.write(f"Recall: {recall:.4f}\n")
            f.write(f"F1-Score: {f1:.4f}\n\n")
            f.write("CONFUSION MATRIX\n")
            f.write("-" * 60 + "\n")
            f.write(str(cm_df) + "\n\n")
            f.write("DETAILED CLASSIFICATION REPORT\n")
            f.write("-" * 60 + "\n")
            f.write(classification_report(true_labels, predictions, target_names=["Fake", "Real"]))
        logger.info("Saved evaluation report to %s", report_path)
    
    update_progress_log(f"Evaluated model on test set. Accuracy: {accuracy:.4f}")
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm,
        "classification_report": report,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned model and generate confusion matrix.")
    parser.add_argument(
        "--test-csv",
        type=str,
        default=str(PROCESSED_DIR / "test.csv"),
        help="Path to test CSV file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save confusion matrix and report (optional)",
    )
    args = parser.parse_args()
    
    test_path = Path(args.test_csv)
    if not test_path.exists():
        raise FileNotFoundError(f"Test CSV not found: {test_path}")
    
    output_dir = Path(args.output_dir) if args.output_dir else None
    evaluate(test_path, output_dir)


if __name__ == "__main__":
    main()

