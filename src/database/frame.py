from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.frame import Frame

async def create_frame(db: AsyncSession, video_id: int, frame_number: int, frame_path: str) -> Frame:
    frame = Frame(video_id=video_id, frame_number=frame_number, frame_path=frame_path)
    db.add(frame)
    await db.commit()
    await db.refresh(frame)
    return frame

async def get_frame_by_id(db: AsyncSession, frame_id: int) -> Optional[Frame]:
    result = await db.execute(
        select(Frame).where(Frame.id == frame_id)
        .options(selectinload(Frame.inference_frame))
    )
    return result.scalar_one_or_none()

async def update_frame(db: AsyncSession, frame_id: int, frame_number: Optional[int] = None, frame_path: Optional[str] = None) -> Optional[Frame]:
    result = await db.execute(select(Frame).where(Frame.id == frame_id))
    frame = result.scalar_one_or_none()
    if not frame:
        return None
    if frame_number is not None:
        frame.frame_number = frame_number
    if frame_path:
        frame.frame_path = frame_path
    await db.commit()
    await db.refresh(frame)
    return frame

async def delete_frame(db: AsyncSession, frame_id: int) -> bool:
    result = await db.execute(select(Frame).where(Frame.id == frame_id))
    frame = result.scalar_one_or_none()
    if not frame:
        return False
    await db.delete(frame)
    await db.commit()
    return True
