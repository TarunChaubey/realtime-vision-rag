from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.database import init_db
from src.api import video_router, frame_router, inference_router, yolo_router, image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Computer Vision Inference API", lifespan=lifespan)

app.include_router(video_router.router)
app.include_router(frame_router.router)
app.include_router(image_router.router)
# app.include_router(inference_router.router)
app.include_router(yolo_router.router)


@app.get("/health")
async def health_check():
    return {"status": "OK"}
