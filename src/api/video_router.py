import os
import uuid
import aiofiles
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.core.database import get_db
from src.database.video import create_video, get_video_by_id, get_all_videos, update_video, delete_video

router = APIRouter(prefix="/videos", tags=["Videos"])

ALLOWED = {".mp4", ".avi", ".mov", ".mkv"}
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_video(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(status_code=400, detail="Only .mp4, .avi, .mov, .mkv allowed")
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return await create_video(db, file_name=file.filename, file_path=file_path)


@router.get("/")
async def list_videos(db: AsyncSession = Depends(get_db)):
    return await get_all_videos(db)


@router.get("/{video_id}")
async def get_video(video_id: int, db: AsyncSession = Depends(get_db)):
    video = await get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.put("/{video_id}")
async def update_video_endpoint(
    video_id: int,
    file_name: Optional[str] = Form(None),
    file_path: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    video = await update_video(db, video_id, file_name, file_path)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.delete("/{video_id}")
async def delete_video_endpoint(video_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_video(db, video_id):
        raise HTTPException(status_code=404, detail="Video not found")
    return {"message": "Video deleted successfully"}
