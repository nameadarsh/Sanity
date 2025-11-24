"""
Fine-tuning script for DistilBERT on the processed Sanity dataset.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from torch.utils.data import Dataset
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizerFast,
    Trainer,
    TrainingArguments,
)

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


class NewsDataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame, tokenizer: DistilBertTokenizerFast, max_len: int = 256):
        texts = dataframe["text"].astype(str).tolist()
        labels = dataframe["label"].astype(int).tolist()
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding="max_length",
            max_length=max_len,
        )
        self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


def load_datasets(tokenizer: DistilBertTokenizerFast, max_len: int) -> tuple[Dataset, Dataset]:
    train_path = PROCESSED_DIR / "train.csv"
    val_path = PROCESSED_DIR / "val.csv"
    if not train_path.exists() or not val_path.exists():
        raise FileNotFoundError("Processed datasets missing. Run preprocess_data.py first.")

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    return NewsDataset(train_df, tokenizer, max_len), NewsDataset(val_df, tokenizer, max_len)


def compute_metrics(eval_pred) -> Dict[str, float]:
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="binary", zero_division=0
    )
    acc = accuracy_score(labels, predictions)
    return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}


def train_model(epochs: int, batch_size: int, max_len: int, learning_rate: float) -> None:
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)

    train_dataset, val_dataset = load_datasets(tokenizer, max_len)
    training_args = TrainingArguments(
        output_dir=str(BASE_DIR / "model_output"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="eval_f1",
        greater_is_better=True,
        logging_strategy="steps",
        logging_steps=100,
        report_to=None,
        save_safetensors=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    logger.info("Starting training for %s epochs.", epochs)
    update_progress_log("Started DistilBERT fine-tuning run.")
    trainer.train()
    try:
        trainer.save_model(MODEL_DIR)
    except Exception as exc:  # pragma: no cover - windows file lock fallback
        logger.warning("trainer.save_model failed (%s). Saving manually.", exc)
        model.save_pretrained(MODEL_DIR, safe_serialization=False)

    torch.save(model.state_dict(), FINE_TUNED_MODEL_PATH)
    logger.info("Training complete. Model saved to %s", FINE_TUNED_MODEL_PATH)
    update_progress_log("Completed DistilBERT fine-tuning run.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune DistilBERT for fake news detection.")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-len", type=int, default=256)
    parser.add_argument("--lr", type=float, default=3e-5)
    args = parser.parse_args()
    train_model(args.epochs, args.batch_size, args.max_len, args.lr)


if __name__ == "__main__":
    main()

