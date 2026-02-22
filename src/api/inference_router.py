from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.database.inference import create_inference, get_inference_by_id, update_inference, delete_inference

router = APIRouter(prefix="/inferences", tags=["Inferences"])

@router.post("/")
async def create_inference_endpoint(
    frame_id: int = Form(...), class_name: str = Form(...), confidence: float = Form(...),
    x_min: float = Form(...), y_min: float = Form(...),
    x_max: float = Form(...), y_max: float = Form(...),
    polygon: Optional[List[float]] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    return await create_inference(db, frame_id, class_name, confidence, x_min, y_min, x_max, y_max, polygon)

@router.get("/{inference_id}")
async def get_inference_endpoint(inference_id: int, db: AsyncSession = Depends(get_db)):
    inference = await get_inference_by_id(db, inference_id)
    if not inference:
        raise HTTPException(status_code=404, detail="Inference not found")
    return inference

@router.put("/{inference_id}")
async def update_inference_endpoint(
    inference_id: int,
    class_name: Optional[str] = Form(None), confidence: Optional[float] = Form(None),
    x_min: Optional[float] = Form(None), y_min: Optional[float] = Form(None),
    x_max: Optional[float] = Form(None), y_max: Optional[float] = Form(None),
    polygon: Optional[List[float]] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    inference = await update_inference(
        db, inference_id, class_name=class_name, confidence=confidence,
        x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max, polygon=polygon
    )
    if not inference:
        raise HTTPException(status_code=404, detail="Inference not found")
    return inference

@router.delete("/{inference_id}")
async def delete_inference_endpoint(inference_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_inference(db, inference_id):
        raise HTTPException(status_code=404, detail="Inference not found")
    return {"message": "Inference deleted successfully"}
