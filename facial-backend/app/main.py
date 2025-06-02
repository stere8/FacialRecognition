# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.camera import find_all_cameras
# Import routers
from app.routes.recognize import router as recognize_router
from app.routes.faces import router as faces_router
from app.routes.camera import router as camera_router

# Import utils (give the utility a distinct alias)
from app.utils import initialize_database, load_known_faces as preload_encodings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React front end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder for serving registered face images
app.mount(
    "/reference_images",
    StaticFiles(directory="app/reference_images"),
    name="reference_images"
)

@app.on_event("startup")
def on_startup():
    """
    - Initialize SQLite tables if they don't exist.
    - Preload known-face encodings into memory.
    """
    initialize_database()    # creates the table if it’s missing
    preload_encodings()      # calls the util function, not this startup handler

# Register all routers under /api
app.include_router(recognize_router, prefix="/api")
app.include_router(faces_router,    prefix="/api")

app.include_router(camera_router, prefix="/api")
