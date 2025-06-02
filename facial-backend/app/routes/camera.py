# app/routes/camera.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette.responses import StreamingResponse

from app.utils import  find_cameras_indices,use_specific_camera

router = APIRouter(prefix="/camera")

@router.get("/")
async def find_all_cameras():
    camera_indices = find_cameras_indices()

    return {"cameras": camera_indices}

@router.get("/{camera_index}/stream")
async def use_camera(camera_index: int):
    return StreamingResponse(
        use_specific_camera(camera_index),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )