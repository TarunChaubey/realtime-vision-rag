from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.utils.database import get_async_engine, get_async_session, get_async_engine_session
user = "postgres"
password = "postgrespassword"
host = "localhost"
port = "5432"
database = "ai_db"
engine, get_db = get_async_engine_session(user, password, host, port, database)

from src.database.inference import (
    create_inference, get_inference_by_id,
    update_inference, delete_inference
)

router = APIRouter(prefix="/inferences", tags=["Inferences"])


@router.post("/")
async def create_inference_endpoint(
    frame_id: int,
    class_name: str,
    confidence: float,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    polygon: Optional[List[float]] = None,
    db: AsyncSession = Depends(get_db)
):
    return await create_inference(
        db,
        frame_id,
        class_name,
        confidence,
        x_min,
        y_min,
        x_max,
        y_max,
        polygon
    )


@router.get("/{inference_id}")
async def get_inference_endpoint(
    inference_id: int,
    db: AsyncSession = Depends(get_db)
):
    inference = await get_inference_by_id(db, inference_id)
    if not inference:
        raise HTTPException(status_code=404, detail="Inference not found")
    return inference


@router.put("/{inference_id}")
async def update_inference_endpoint(
    inference_id: int,
    class_name: Optional[str] = None,
    confidence: Optional[float] = None,
    x_min: Optional[float] = None,
    y_min: Optional[float] = None,
    x_max: Optional[float] = None,
    y_max: Optional[float] = None,
    polygon: Optional[List[float]] = None,
    db: AsyncSession = Depends(get_db)
):
    inference = await update_inference(
        db,
        inference_id,
        class_name=class_name,
        confidence=confidence,
        x_min=x_min,
        y_min=y_min,
        x_max=x_max,
        y_max=y_max,
        polygon=polygon
    )

    if not inference:
        raise HTTPException(status_code=404, detail="Inference not found")

    return inference


@router.delete("/{inference_id}")
async def delete_inference_endpoint(
    inference_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await delete_inference(db, inference_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inference not found")
    return {"message": "Inference deleted successfully"}