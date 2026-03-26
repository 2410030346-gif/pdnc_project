# Handwriting Web App (Convo Script)

End-to-end Python web application that supports:

1. File to handwriting conversion (.txt/.docx/.pdf -> generated handwriting image)
2. Handwriting image to digital text conversion (OCR)
3. Handwritten digit recognition using a trained CNN model
4. Downloading generated handwriting as PDF or DOCX

This README documents the complete project flow, implementation details, tech stack, and tools used from setup to execution.

## 1. Project Overview

This project combines classical web development (Flask + HTML/CSS/JS) with machine learning and OCR pipelines.

Core idea:

- Input typed document text or a handwritten image.
- Convert typed text into handwriting-style output with selectable styles/backgrounds.
- Convert handwritten image content back into editable digital text using Tesseract OCR.
- Provide downloadable artifacts (PDF/DOCX) for generated output.

## 2. Tech Stack And Tools

### Programming Language

- Python 3.11
- HTML5
- CSS3
- JavaScript (browser-side)

### ML / Data / Vision Libraries

- TensorFlow
- Keras
- NumPy
- OpenCV (opencv-python)
- scikit-learn
- pandas
- matplotlib
- Pillow (PIL)

### OCR / Document Processing

- pytesseract
- Tesseract OCR engine (system dependency)
- python-docx
- pypdf

### Backend / Web

- Flask
- python-dotenv

### Development Environment And Runtime Tools

- Python virtual environment (.venv311)
- Windows PowerShell
- pip

## 3. Dependency List

Dependencies defined in requirements.txt:

- numpy
- pandas
- matplotlib
- opencv-python
- tensorflow
- keras
- scikit-learn
- flask
- pillow
- python-docx
- pypdf
- python-dotenv
- pytesseract

## 4. Project Structure

```
handwriting_web_app/
  README.md
  requirements.txt
  data/
  models/
    recognition_model.h5
  src/
    evaluate.py
    predict.py
    preprocess.py
    recognition.py
    synthesis.py
    train_recognition.py
    train_synthesis.py
  web/
    app.py
    static/
      script.js
      style.css
    templates/
      index.html
```

## 5. Implementation Flow (Start To End)

### Phase A: Environment Setup

1. Created Python 3.11 virtual environment.
2. Installed dependencies from requirements.txt.
3. Organized code into src (ML/logic) and web (Flask/UI).

### Phase B: Handwritten Digit Recognition Pipeline

1. Implemented CNN model architecture in src/recognition.py.
2. Used Keras MNIST dataset in src/train_recognition.py.
3. Preprocessed MNIST images to shape (28, 28, 1) and normalized to [0, 1].
4. Trained model for 5 epochs.
5. Saved trained model to models/recognition_model.h5.
6. Added inference utility in src/predict.py:
   - Accepts image path or numpy array.
   - Preprocesses to 28x28 grayscale tensor.
   - Loads model and returns predicted class + confidence.
7. Added evaluation script src/evaluate.py for test loss/accuracy.

### Phase C: Handwriting Synthesis Pipeline

1. Implemented lightweight handwriting renderer in src/synthesis.py.
2. Added style presets:
   - cursive, neat, marker, mono, signature.
3. Added paper presets:
   - plain, warm, blue, ruled/lines, grid, dots.
4. Implemented text wrapping and dynamic canvas height.
5. Added optional save-to-file behavior.

### Phase D: Flask Backend Integration

1. Implemented backend in web/app.py.
2. Added startup configuration:
   - Loads .env using python-dotenv.
   - Configures Flask secret key.
   - Auto-detects Windows Tesseract path when available.
3. Added document text extraction for:
   - .txt (UTF-8 decode)
   - .docx (paragraphs, tables, headers, footers)
   - .pdf (page-level extraction via pypdf)
4. Added OCR preprocessing flow:
   - Decode image with OpenCV
   - Grayscale + denoise + adaptive threshold
   - OCR with pytesseract

### Phase E: Frontend UX Integration

1. Built UI in web/templates/index.html.
2. Added landing animation and branded layout.
3. Added mode switch:
   - File to Handwriting
   - Handwriting to Text
4. Added paper/style pickers synced with backend request payload.
5. Added preview panel for extracted text and generated image.
6. Added download buttons for PDF and DOCX output.

### Phase F: End-To-End User Flow

Flow 1: File to Handwriting

1. User uploads .txt/.docx/.pdf.
2. Frontend submits multipart form to /convert-file.
3. Backend extracts text.
4. Backend generates handwriting image with selected styles.
5. Backend returns:
   - extracted_text
   - base64 image_data
6. Frontend updates text preview + handwriting preview.
7. User downloads PDF/DOCX via /download-handwriting.

Flow 2: Handwriting to Text

1. User uploads handwritten image.
2. Frontend sends image to /handwriting-to-text.
3. Backend runs OCR preprocessing + Tesseract.
4. Backend returns extracted text.
5. Frontend shows editable digital text in preview.

Flow 3: Digit Prediction API (ML)

1. User/client uploads image to /predict or /recognize.
2. Backend preprocesses image to model format.
3. Backend loads recognition_model.h5.
4. Backend returns predicted digit (and confidence in /predict).

## 6. API Endpoints

### GET /

- Serves the main web interface.

### GET /health

- Health check endpoint.
- Response: {"status": "ok"}

### POST /convert-file

- Input: file + paperStyle + handwritingStyle
- Supports file types: .txt, .docx, .pdf
- Output: extracted text + generated image (base64)

### POST /handwriting-to-text

- Input: handwritten image file
- Output: extracted_text from OCR

### POST /download-handwriting

- Input: text + format(pdf/docx) + paperStyle + handwritingStyle
- Output: downloadable PDF or DOCX

### POST /predict

- Input: image file
- Output: predicted digit + confidence

### POST /recognize

- Input: image file
- Output: recognized_digit

### POST /generate

- Input: JSON with text + style options
- Output: generated PNG stream

### POST /synthesize

- Input: form text + style options
- Output: generated PNG file response

## 7. Setup And Run (Windows PowerShell)

Run these commands from the handwriting_web_app directory:

```powershell
py -3.11 -m venv .venv311
.\.venv311\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the app:

```powershell
$env:PYTHONPATH=(Get-Location).Path
python web/app.py
```

Open in browser:

- http://127.0.0.1:5000

## 8. Model Training And Evaluation Commands

Train recognition model:

```powershell
python src/train_recognition.py
```

Evaluate recognition model:

```powershell
python src/evaluate.py
```

Run single-image prediction:

```powershell
python src/predict.py path\to\image.png
```

Initialize synthesis script:

```powershell
python src/train_synthesis.py
```

## 9. Implementation Notes

- preprocess.py currently contains placeholders for future preprocessing abstraction.
- web/static/script.js and web/static/style.css exist, but the current UI behavior and styling are primarily implemented inline in templates/index.html.
- OCR quality depends on input image quality and local Tesseract installation.
- For Windows, app.py attempts to use C:/Program Files/Tesseract-OCR/tesseract.exe automatically.

## 10. Future Improvements

1. Replace rule-based synthesis with a learned handwriting generation model.
2. Add unit/integration tests for API endpoints.
3. Move inline CSS/JS from template into static assets for maintainability.
4. Add authentication and per-user file/session management.
5. Add Docker support and production WSGI deployment (gunicorn/waitress).

## 11. Summary

This project is implemented as a complete ML-enabled Flask application with two-way handwriting workflows:

- typed documents -> handwriting output
- handwritten images -> digital text

It includes training/evaluation/inference for digit recognition, customizable handwriting rendering, OCR conversion, and export capabilities (PDF/DOCX) inside a single web product flow.
