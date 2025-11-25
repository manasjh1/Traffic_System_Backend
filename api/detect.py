from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np
from utils.ocr_reader import extract_plate_text
from database.save_log import save_log
import time

router = APIRouter()

# Load YOLO Model
model = YOLO("models/Number_plate_model.pt")


@router.post("/detect/")
async def detect_number_plate(file: UploadFile = File(...)):
    """
    Detects number plates using YOLO + EasyOCR and saves logs to Supabase (REST).
    """

    # Read uploaded file
    image_bytes = await file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid image format"}

    results = model(frame)
    detections = []

    # Process YOLO results
    for box in results[0].boxes:

        # Bounding box
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])

        # Crop number plate
        crop = frame[y1:y2, x1:x2]

        # OCR text
        plate_text = extract_plate_text(crop)

        # Prepare detection
        detection = {
            "class_id": class_id,
            "confidence": round(confidence, 3),
            "bounding_box": [x1, y1, x2, y2],
            "plate_text": plate_text,
            "timestamp": time.strftime("%H:%M:%S")
        }

        detections.append(detection)

        # --------------------------
        # AUTO SAVE TO SUPABASE
        # --------------------------
        save_log(
            vehicle_type="Unknown",
            speed=0,
            helmet_status="Unknown",
            violation_type="Unknown",
            plate=plate_text
        )

    if len(detections) == 0:
        return {
            "message": "No number plate detected",
            "timestamp": time.strftime("%H:%M:%S")
        }

    return {
        "message": "Detection successful",
        "detections": detections
    }

