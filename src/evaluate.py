"""Evaluate the saved handwriting recognition model on MNIST test data."""

from pathlib import Path

from keras.datasets import mnist
from keras.models import load_model


def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]
    model_path = root_dir / "models" / "recognition_model.h5"

    if not model_path.exists():
        print(f"Model not found at: {model_path}")
        print("Train first: python src/train_recognition.py")
        return

    (_, _), (x_test, y_test) = mnist.load_data()
    x_test = x_test.reshape(-1, 28, 28, 1) / 255.0

    model = load_model(model_path)
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)

    print(f"Model: {model_path}")
    print(f"Test loss: {loss:.4f}")
    print(f"Test accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
