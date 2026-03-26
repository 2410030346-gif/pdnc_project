"""Run inference with the trained recognition model on a single image."""

from pathlib import Path
import argparse
from typing import Union

import numpy as np
from keras.models import load_model
from PIL import Image


def preprocess_image(image_path: Path) -> np.ndarray:
    """Load image, convert to grayscale 28x28, normalize, and add batch/channel dims."""
    image = Image.open(image_path).convert("L").resize((28, 28))
    array = np.array(image, dtype="float32") / 255.0
    array = array.reshape(1, 28, 28, 1)
    return array


def preprocess_array(image_array: np.ndarray) -> np.ndarray:
    """Preprocess image arrays from web requests into model-ready tensor."""
    array = image_array
    if array.ndim == 3:
        array = np.mean(array, axis=2)
    array = np.asarray(array, dtype="float32")
    image = Image.fromarray(array).resize((28, 28)).convert("L")
    array = np.array(image, dtype="float32") / 255.0
    return array.reshape(1, 28, 28, 1)


def recognize_digit(
    image_input: Union[str, Path, np.ndarray],
    model_path: Union[str, Path, None] = None,
) -> tuple[int, float]:
    """Predict a single handwritten digit from path or numpy array input."""
    model_file = Path(model_path) if model_path else Path(__file__).resolve().parents[1] / "models" / "recognition_model.h5"
    if not model_file.exists():
        raise FileNotFoundError(f"Model not found at: {model_file}")

    model = load_model(model_file)

    if isinstance(image_input, (str, Path)):
        x = preprocess_image(Path(image_input))
    else:
        x = preprocess_array(image_input)

    probs = model.predict(x, verbose=0)[0]
    pred_class = int(np.argmax(probs))
    confidence = float(np.max(probs))
    return pred_class, confidence


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict handwritten digit from image")
    parser.add_argument("image", type=str, help="Path to input image")
    parser.add_argument(
        "--model",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "models" / "recognition_model.h5"),
        help="Path to trained model file",
    )
    args = parser.parse_args()

    model_path = Path(args.model)
    image_path = Path(args.image)

    if not image_path.exists():
        print(f"Image not found at: {image_path}")
        return

    try:
        pred_class, confidence = recognize_digit(image_path, model_path)
    except FileNotFoundError as exc:
        print(exc)
        print("Train first: python src/train_recognition.py")
        return

    print(f"Predicted digit: {pred_class}")
    print(f"Confidence: {confidence:.4f}")


if __name__ == "__main__":
    main()
