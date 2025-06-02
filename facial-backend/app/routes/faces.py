# app/routes/faces.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.utils import add_reference_face, get_all_faces

router = APIRouter(prefix="/faces")


@router.get("/")
async def list_faces():
    """
    GET /faces/
    - Returns a list of all registered reference faces:
      [{ "name": "...", "image_url": "/reference_images/filename.jpg" }, ...]
    """
    faces = get_all_faces()
    # Build full URL path for each image
    return [
        {"name": face["name"], "image_url": f"/reference_images/{face['image_path']}"}
        for face in faces
    ]


@router.post("/save")
async def register_face(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    POST /faces/register
    - Accepts:
      • name (form field)
      • file (form file field)
    - Saves the image, computes its encoding, stores in SQLite.
    - Returns: { "status": "ok", "name": "<registered name>", "image_path": "<filename>" }
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file upload.")

    try:
        image_filename = add_reference_face(name, contents, file.filename)
    except ValueError as e:
        return {"status": "ok", "name": name, "image_path": e}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

    return {"status": "ok", "name": name, "image_path": image_filename}
