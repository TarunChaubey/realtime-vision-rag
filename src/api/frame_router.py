from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.database.frame import create_frame, get_frame_by_id, update_frame, delete_frame

router = APIRouter(prefix="/frames", tags=["Frames"])

@router.post("/")
async def create_frame_endpoint(
    video_id: int = Form(...), frame_number: int = Form(...), frame_path: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    return await create_frame(db, video_id, frame_number, frame_path)

@router.get("/{frame_id}")
async def get_frame_endpoint(frame_id: int, db: AsyncSession = Depends(get_db)):
    frame = await get_frame_by_id(db, frame_id)
    if not frame:
        raise HTTPException(status_code=404, detail="Frame not found")
    return frame

@router.put("/{frame_id}")
async def update_frame_endpoint(
    frame_id: int,
    frame_number: Optional[int] = Form(None), frame_path: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    frame = await update_frame(db, frame_id, frame_number, frame_path)
    if not frame:
        raise HTTPException(status_code=404, detail="Frame not found")
    return frame

@router.delete("/{frame_id}")
async def delete_frame_endpoint(frame_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_frame(db, frame_id):
        raise HTTPException(status_code=404, detail="Frame not found")
    return {"message": "Frame deleted successfully"}
