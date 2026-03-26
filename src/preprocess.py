"""Preprocessing utilities for handwriting images and text."""

from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def preprocess_image(image_path: str):
    """Load and preprocess an image for model input."""
    raise NotImplementedError("Implement image preprocessing logic.")


def preprocess_text(text: str):
    """Normalize text labels for training/inference."""
    raise NotImplementedError("Implement text preprocessing logic.")
