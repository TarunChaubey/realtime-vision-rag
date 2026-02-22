import os
import uuid
import aiofiles
from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_db
from src.database.inference import save_inference_output
from src.database.image import get_image_by_id
from src.database.frame import get_frame_by_id
from src.inference_pipeline.yolo_inference import YoloBackend
from src.inference_pipeline.base import InferenceBackend

router = APIRouter(prefix="/infer", tags=["Inference"])

# --- Backend registry: swap or extend here ---
_backends: dict[str, InferenceBackend] = {
    "yolo": YoloBackend(settings.YOLO_MODEL_PATH, device="cpu"),
}

ALLOWED_IMG = {".jpg", ".jpeg", ".png"}
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


def _get_backend(name: str) -> InferenceBackend:
    if name not in _backends:
        raise HTTPException(status_code=400, detail=f"Unknown backend '{name}'. Available: {list(_backends)}")
    return _backends[name]


async def _save_temp(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_IMG:
        raise HTTPException(status_code=400, detail="Only .jpg, .jpeg, .png allowed")
    path = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    async with aiofiles.open(path, "wb") as f:
        await f.write(await file.read())
    return path


@router.post("/image")
async def infer_on_image(
    file: UploadFile = File(...),
    image_id: int = Form(...),
    task: Literal["detect", "segment"] = Form("detect"),
    backend: str = Form("yolo"),
    db: AsyncSession = Depends(get_db),
):
    """Run inference on an uploaded image. image_id must exist in the images table."""
    if not await get_image_by_id(db, image_id):
        raise HTTPException(status_code=404, detail="Image not found")

    svc = _get_backend(backend)
    path = await _save_temp(file)
    try:
        output = await svc.predict(path) if task == "detect" else await svc.segment(path)
        saved = await save_inference_output(db, output, source_type="image", source_id=image_id)
        return {"detections": len(saved), "results": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(path):
            os.remove(path)


@router.post("/frame")
async def infer_on_frame(
    file: UploadFile = File(...),
    frame_id: int = Form(...),
    task: Literal["detect", "segment"] = Form("detect"),
    backend: str = Form("yolo"),
    db: AsyncSession = Depends(get_db),
):
    """Run inference on a frame image. frame_id must exist in the frames table."""
    if not await get_frame_by_id(db, frame_id):
        raise HTTPException(status_code=404, detail="Frame not found")

    svc = _get_backend(backend)
    path = await _save_temp(file)
    try:
        output = await svc.predict(path) if task == "detect" else await svc.segment(path)
        saved = await save_inference_output(db, output, source_type="frame", source_id=frame_id)
        return {"detections": len(saved), "results": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(path):
            os.remove(path)
