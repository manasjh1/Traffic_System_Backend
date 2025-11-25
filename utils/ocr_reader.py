import easyocr
import cv2
import numpy as np
import re

# Initialize EasyOCR reader only once (performance optimization)
# gpu=False is safer unless your device has CUDA
reader = easyocr.Reader(['en'], gpu=False)


def preprocess_plate(plate_img):
    """
    Applies preprocessing to improve OCR accuracy.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # Resize – improves OCR accuracy on small plates
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 8
    )

    return thresh


def extract_plate_text(plate_img):
    """
    Extracts number plate text using EasyOCR.
    Input: Cropped plate image (RGB/BGR format)
    Output: Clean number plate string (e.g., 'UP15BY7890')
    """

    if plate_img is None or plate_img.size == 0:
        return "UNKNOWN"

    # Preprocess image
    processed_img = preprocess_plate(plate_img)

    # Run EasyOCR
    results = reader.readtext(processed_img)

    if not results:
        return "UNKNOWN"

    # Extract the detected text (best match = first result)
    text = results[0][1]

    # Clean text (keep only alphabets and numbers)
    cleaned_text = re.sub(r'[^A-Z0-9]', '', text.upper())

    # Remove obvious OCR noise
    if len(cleaned_text) < 4:  # Plates cannot be too short
        return "UNKNOWN"

    return cleaned_text
