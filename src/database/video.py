from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.video import Video
from src.models.frame import Frame

async def create_video(db: AsyncSession, file_name: str, file_path: str) -> Video:
    video = Video(file_name=file_name, file_path=file_path)
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video

async def get_video_by_id(db: AsyncSession, video_id: int) -> Optional[Video]:
    result = await db.execute(
        select(Video).where(Video.id == video_id)
        .options(selectinload(Video.frames).selectinload(Frame.inference_frame))
    )
    return result.scalar_one_or_none()

async def get_all_videos(db: AsyncSession) -> list[Video]:
    result = await db.execute(select(Video))
    return result.scalars().all()

async def update_video(db: AsyncSession, video_id: int, file_name: Optional[str] = None, file_path: Optional[str] = None) -> Optional[Video]:
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        return None
    if file_name:
        video.file_name = file_name
    if file_path:
        video.file_path = file_path
    await db.commit()
    await db.refresh(video)
    return video

async def delete_video(db: AsyncSession, video_id: int) -> bool:
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        return False
    await db.delete(video)
    await db.commit()
    return True
