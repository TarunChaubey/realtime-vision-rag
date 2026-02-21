from typing import Optional
from fastapi import APIRouter, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.inference import (
    create_frame,
    get_frame_by_id,
    update_frame,
    delete_frame
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
router = APIRouter(prefix="/frames", tags=["Frames"])

# Create Frame
@router.post("/add_frame")
async def create_frame_endpoint(
    video_id: int = Form(...),
    frame_number: int = Form(...),
    frame_path: str = Form(...),
):
    async with Session() as db:
        return await create_frame(db, video_id, frame_number, frame_path)


# Get Frame by ID
@router.get("/{frame_id}")
async def get_frame_endpoint(
    frame_id: int
):
    async with Session() as db:
        frame = await get_frame_by_id(db, frame_id)
        if not frame:
            raise HTTPException(status_code=404, detail="Frame not found")
        return frame

# Update Frame
@router.put("/{frame_id}")
async def update_frame_endpoint(
    frame_id: int,
    frame_number: Optional[int] = Form(None),
    frame_path: Optional[str] = Form(None),
):
    async with Session() as db:
        frame = await update_frame(db, frame_id, frame_number, frame_path)
        if not frame:
            raise HTTPException(status_code=404, detail="Frame not found")
        return frame


# Delete Frame
@router.delete("/{frame_id}")
async def delete_frame_endpoint(
    frame_id: int,
):
    async with Session() as db:
        deleted = await delete_frame(db, frame_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Frame not found")
        return {"message": "Frame deleted successfully"}