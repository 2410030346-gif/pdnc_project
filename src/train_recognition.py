"""Training entrypoint for recognition model"""

from pathlib import Path

from recognition import build_recognition_model
from keras.datasets import mnist

if __name__ == "__main__":
    # Load MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Preprocess data
    x_train = x_train.reshape(-1,28,28,1) / 255.0
    x_test = x_test.reshape(-1,28,28,1) / 255.0

    # Build model
    model = build_recognition_model()

    # Train model
    model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

    # Save model in project models directory regardless of current working directory
    model_output_path = Path(__file__).resolve().parents[1] / "models" / "recognition_model.h5"
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(model_output_path)

    print("Recognition model trained and saved successfully!")