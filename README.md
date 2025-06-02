Facial Recognition Web App
Tech Stack:

Backend: FastAPI, SQLite, face_recognition, OpenCV

Frontend: React, Tailwind CSS

Features
Register Faces: Upload one‐face image + name → stored in SQLite.

View All Faces: 96×96 thumbnails grid of registered faces.

Identify Faces: Upload image → returns matched names + bounding boxes.

Live Camera Feed: List camera indices → stream MJPEG via <img>.

Quick Setup
Backend
Python 3.11 venv → install dependencies:

bash
Copy
Edit
cd facial-backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn face-recognition opencv-python pillow
Run:

bash
Copy
Edit
uvicorn app.main:app --reload
Database and reference_images/ auto‐created.

Frontend
Install & run:

bash
Copy
Edit
cd facial-frontend
npm install
npm run dev
Ensure src/settings.js has:

js
Copy
Edit
export const BASE_URL = "http://localhost:8000";
Usage
All Faces: Click “All Faces” tab → shows stored faces.

Add Person: Upload + name → “Save Person.”

Identify: Upload → “Identify Face.”

Camera: Select index → live MJPEG feed in <img src="/api/camera/{index}/stream">.

API Endpoints
GET /api/faces/ → list { name, image_url }.

POST /api/faces/save → form fields: name, file.

POST /api/recognize → form field: file.

GET /api/camera/ → { cameras: [0,1,…] }.

GET /api/camera/{index}/stream → MJPEG stream.
