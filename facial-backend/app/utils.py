# app/utils.py

import os
import sqlite3
import json
import uuid
import io
from http.client import HTTPException

import face_recognition
from PIL import Image
import numpy as np
import cv2
# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "face_data.db")
REF_DIR = os.path.join(BASE_DIR, "reference_images")

# Ensure reference_images directory exists
os.makedirs(REF_DIR, exist_ok=True)


def initialize_database():
    """
    Create the SQLite database and the 'faces' table if they don't exist.
    Columns:
      - id: auto-increment primary key
      - name: text label
      - encoding: JSON-serialized list of 128 floats
      - image_path: filename under reference_images/
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_all_faces():
    """
    Return a list of dicts for every registered face:
      [{'name': ..., 'image_path': ...}, ...]
    Used by the GET /faces endpoint to build image URLs.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, image_path FROM faces")
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "image_path": r[1]} for r in rows]


def add_reference_face(name: str, image_bytes: bytes, original_filename: str):
    """
    Register a new reference face:
      1. Compute its encoding (must be exactly one face).
      2. Save the image into reference_images/ with a unique filename.
      3. Insert (name, encoding JSON, image_path) into SQLite.
    Returns the saved filename.
    Raises ValueError if no face or multiple faces are found.
    """
    # Load image from bytes and detect face(s)
    img_stream = io.BytesIO(image_bytes)
    img = face_recognition.load_image_file(img_stream)
    locations = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, locations)

    if len(encodings) != 1:
        raise ValueError("Uploaded image must contain exactly one face.")
    encoding_list = encodings[0].tolist()

    # Save image file
    ext = os.path.splitext(original_filename)[1] or ".jpg"
    unique_name = f"{uuid.uuid4()}{ext}"
    save_path = os.path.join(REF_DIR, unique_name)
    with open(save_path, "wb") as f:
        f.write(image_bytes)

    # Insert into SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO faces (name, encoding, image_path) VALUES (?, ?, ?)",
        (name, json.dumps(encoding_list), unique_name)
    )
    conn.commit()
    conn.close()

    return unique_name


def load_known_faces():
    """
    Load all known face encodings from SQLite into memory.
    Returns a list of tuples: [(name, np.ndarray(128,)), ...]
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, encoding FROM faces")
    rows = c.fetchall()
    conn.close()

    known = []
    for name, encoding_json in rows:
        encoding_list = json.loads(encoding_json)
        known.append((name, np.array(encoding_list)))
    return known


def recognize_faces_in_image(image_bytes: bytes, tolerance: float = 0.6):
    """
    Given raw image bytes:
      1. Detect face locations & encodings.
      2. Compare each encoding against known faces.
    Returns:
      - matches: list of matched names (or "Unknown" if no match under tolerance).
      - boxes: list of dicts {top, right, bottom, left} for each face.
    """
    # Load and locate faces in the uploaded image
    img_stream = io.BytesIO(image_bytes)
    img = face_recognition.load_image_file(img_stream)
    locations = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, locations)

    if not encodings:
        # No faces detected
        return [], []

    # Load known faces once (could be cached on startup if desired)
    known = load_known_faces()
    known_names = [item[0] for item in known]
    known_encodings = [item[1] for item in known]

    matches = []
    for face_encoding in encodings:
        if known_encodings:
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_idx = np.argmin(distances)
            if distances[best_idx] <= tolerance:
                matches.append(known_names[best_idx])
            else:
                matches.append("Unknown")
        else:
            matches.append("Unknown")

    # Build boxes output from locations
    boxes = []
    for (top, right, bottom, left) in locations:
        boxes.append({"top": top, "right": right, "bottom": bottom, "left": left})

    return matches, boxes


def find_cameras_indices():
    camera_indices = []
    for i in range(1000):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_indices.append(i)
            cap.release()
        else:
            cap.release()

    return camera_indices


def use_specific_camera(id):
    cap = cv2.VideoCapture(id)

    if not cap.isOpened():
        raise HTTPException(status_code=404, detail="Camera not found")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + frame_bytes
                    + b"\r\n"
            )

    finally:
        cap.release()