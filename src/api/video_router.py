from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.inference import (
    create_video,
    get_video_by_id,
    get_all_videos,
    update_video,
    delete_video
)

from src.utils.database import get_async_engine_session

# -------------------------
# Database setup
# -------------------------
user = "postgres"
password = "postgrespassword"
host = "localhost"
port = "5432"
database = "ai_db"

# get_db is a dependency function without extra required parameters
engine, Session = get_async_engine_session(user, password, host, port, database)

# Router setup
router = APIRouter(prefix="/videos", tags=["Videos"])

# Create Video Endpoint
router = APIRouter(prefix="/videos", tags=["Videos"])

# Create Video Endpoint
@router.post("/add_video")
async def create_video_endpoint(
    file_name: str = Form(...),
    file_path: str = Form(...),
):
    async with Session() as db:
        return await create_video(db, file_name, file_path)

# Get Video by ID
@router.get("/{video_id}")
async def get_video_endpoint(
    video_id: int
):
    async with Session() as db:
        video = await get_video_by_id(db, video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video

# Get All Videos
@router.get("/")
async def get_all_videos_endpoint(
):
    async with Session() as db:
        return await get_all_videos(db)

# Update Video
@router.put("/{video_id}")
async def update_video_endpoint(
    video_id: int,
    file_name: Optional[str] = Form(None),
    file_path: Optional[str] = Form(None),
):
    async with Session() as db:
        video = await update_video(db, video_id, file_name, file_path)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video

# Delete Video
@router.delete("/{video_id}")
async def delete_video_endpoint(
    video_id: int,
):
    async with Session() as db:
        deleted = await delete_video(db, video_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Video not found")
        return {"message": "Video deleted successfully"}