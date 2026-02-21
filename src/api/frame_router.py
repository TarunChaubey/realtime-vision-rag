from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.utils.database import get_async_engine, get_async_session, get_async_engine_session
user = "postgres"
password = "postgrespassword"
host = "localhost"
port = "5432"
database = "ai_db"
engine, get_db = get_async_engine_session(user, password, host, port, database)
from src.database.inference import (
    create_frame, get_frame_by_id,
    update_frame, delete_frame
)

router = APIRouter(prefix="/frames", tags=["Frames"])


@router.post("/")
async def create_frame_endpoint(
    video_id: int,
    frame_number: int,
    frame_path: str,
    db: AsyncSession = Depends(get_db)
):
    return await create_frame(db, video_id, frame_number, frame_path)


@router.get("/{frame_id}")
async def get_frame_endpoint(
    frame_id: int,
    db: AsyncSession = Depends(get_db)
):
    frame = await get_frame_by_id(db, frame_id)
    if not frame:
        raise HTTPException(status_code=404, detail="Frame not found")
    return frame


@router.put("/{frame_id}")
async def update_frame_endpoint(
    frame_id: int,
    frame_number: Optional[int] = None,
    frame_path: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    frame = await update_frame(db, frame_id, frame_number, frame_path)
    if not frame:
        raise HTTPException(status_code=404, detail="Frame not found")
    return frame


@router.delete("/{frame_id}")
async def delete_frame_endpoint(
    frame_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await delete_frame(db, frame_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Frame not found")
    return {"message": "Frame deleted successfully"}