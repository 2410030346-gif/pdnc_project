"""Training entrypoint for the handwriting synthesis model."""

from synthesis import build_synthesis_model


if __name__ == "__main__":
    model = build_synthesis_model()
    print("Synthesis model initialized:", type(model).__name__)
