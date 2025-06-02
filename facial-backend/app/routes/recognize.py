# app/routes/recognize.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils import recognize_faces_in_image

router = APIRouter()


@router.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """
    POST /recognize
    - Accepts: multipart/form-data with a single 'file' (image).
    - Returns: { "names": [...], "boxes": [...] }.
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file upload.")

    try:
        names, boxes = recognize_faces_in_image(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition error: {str(e)}")

    return {"names": names, "boxes": boxes}
