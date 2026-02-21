from typing import Optional, List
from fastapi import APIRouter, HTTPException, Form

from src.database.inference import (
    create_inference,
    get_inference_by_id,
    update_inference,
    delete_inference
)

from src.utils.database import get_async_engine_session

# Database setup
user = "postgres"
password = "postgrespassword"
host = "localhost"
port = "5432"
database = "ai_db"

engine, Session = get_async_engine_session(user, password, host, port, database)

# Router setup
router = APIRouter(prefix="/inferences", tags=["Inferences"])


# Create Inference
@router.post("/add_inference")
async def create_inference_endpoint(
    frame_id: int = Form(...),
    class_name: str = Form(...),
    confidence: float = Form(...),
    x_min: float = Form(...),
    y_min: float = Form(...),
    x_max: float = Form(...),
    y_max: float = Form(...),
    polygon: Optional[List[float]] = Form(None),
):
    async with Session() as db:
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


# Get Inference by ID
@router.get("/{inference_id}")
async def get_inference_endpoint(
    inference_id: int
):
    async with Session() as db:
        inference = await get_inference_by_id(db, inference_id)
        if not inference:
            raise HTTPException(status_code=404, detail="Inference not found")
        return inference

# Update Inference
@router.put("/{inference_id}")
async def update_inference_endpoint(
    inference_id: int,
    class_name: Optional[str] = Form(None),
    confidence: Optional[float] = Form(None),
    x_min: Optional[float] = Form(None),
    y_min: Optional[float] = Form(None),
    x_max: Optional[float] = Form(None),
    y_max: Optional[float] = Form(None),
    polygon: Optional[List[float]] = Form(None),
):
    async with Session() as db:
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


# Delete Inference
@router.delete("/{inference_id}")
async def delete_inference_endpoint(
    inference_id: int,
):
    async with Session() as db:
        deleted = await delete_inference(db, inference_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Inference not found")
        return {"message": "Inference deleted successfully"}