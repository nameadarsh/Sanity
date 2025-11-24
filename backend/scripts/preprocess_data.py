"""
Data preprocessing pipeline for the Sanity project.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

try:
    from ..utils import get_logger, update_progress_log
except ImportError:  # pragma: no cover - script mode
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from utils import get_logger, update_progress_log

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

logger = get_logger(__name__)


def _ensure_nltk_resources() -> None:
    """Download required NLTK resources if missing."""
    resources = ["punkt", "punkt_tab", "wordnet", "stopwords", "omw-1.4"]
    for resource in resources:
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)


def load_datasets() -> pd.DataFrame:
    """Load and merge real/fake datasets."""
    real_path = RAW_DIR / "real.csv"
    fake_path = RAW_DIR / "fake.csv"
    if not real_path.exists() or not fake_path.exists():
        raise FileNotFoundError("Missing raw CSV files in backend/data/raw/")

    real_df = pd.read_csv(real_path)
    fake_df = pd.read_csv(fake_path)
    real_df["label"] = 1
    fake_df["label"] = 0

    df = pd.concat([real_df, fake_df], ignore_index=True)
    logger.info("Loaded dataset with %s rows.", len(df))
    update_progress_log("Loaded raw datasets.")
    return df


def clean_text_column(df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
    """Clean text column according to project spec."""
    _ensure_nltk_resources()
    lemmatizer = WordNetLemmatizer()
    stops = set(stopwords.words("english"))

    def _clean(text: str) -> str:
        text = str(text).lower()
        text = re.sub(r"http\\S+|www\\.\\S+", " ", text)
        text = re.sub(r"[^a-z\\s]", " ", text)
        tokens = [tok for tok in word_tokenize(text) if tok not in stops and len(tok) > 2]
        lemmas = [lemmatizer.lemmatize(tok) for tok in tokens]
        return " ".join(lemmas)

    df = df.copy()
    df[text_column] = df[text_column].fillna("").apply(_clean)
    logger.info("Cleaned text column.")
    update_progress_log("Cleaned and normalized text.")
    return df


def split_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split dataset into train/val/test (70/15/15)."""
    train_df, temp_df = train_test_split(df, test_size=0.30, stratify=df["label"], random_state=42)
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, stratify=temp_df["label"], random_state=42
    )
    logger.info("Split dataset: train=%s, val=%s, test=%s", len(train_df), len(val_df), len(test_df))
    update_progress_log("Split dataset into train/val/test.")
    return train_df, val_df, test_df


def save_splits(train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    """Persist processed splits."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(PROCESSED_DIR / "train.csv", index=False)
    val_df.to_csv(PROCESSED_DIR / "val.csv", index=False)
    test_df.to_csv(PROCESSED_DIR / "test.csv", index=False)
    logger.info("Saved processed datasets.")
    update_progress_log("Saved processed datasets to backend/data/processed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess raw news datasets.")
    parser.add_argument("--text-column", default="text", help="Name of the text column to clean.")
    args = parser.parse_args()

    df = load_datasets()
    df = clean_text_column(df, text_column=args.text_column)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    train_df, val_df, test_df = split_dataset(df)
    save_splits(train_df, val_df, test_df)
    logger.info("Preprocessing complete.")
    update_progress_log("Completed data preprocessing workflow.")


if __name__ == "__main__":
    main()

