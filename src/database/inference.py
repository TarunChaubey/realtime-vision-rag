from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP, text,func,DateTime,TEXT,Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import ARRAY
from src.sechema.inference import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

async def create_video(
    db: AsyncSession,
    file_name: str,
    file_path: str
):
    new_video = Video(
        file_name=file_name,
        file_path=file_path
    )
    db.add(new_video)
    await db.commit()
    await db.refresh(new_video)
    return new_video

async def get_video_by_id(
    db: AsyncSession,
    video_id: int
):
    result = await db.execute(
        select(Video)
        .where(Video.id == video_id)
        .options(
            selectinload(Video.frames)
            .selectinload(Frame.inference_results)
        )
    )
    return result.scalar_one_or_none()

async def get_all_videos(db: AsyncSession):
    result = await db.execute(select(Video))
    return result.scalars().all()

async def update_video(
    db: AsyncSession,
    video_id: int,
    file_name: Optional[str] = None,
    file_path: Optional[str] = None
):
    result = await db.execute(
        select(Video).where(Video.id == video_id)
    )
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

async def delete_video(
    db: AsyncSession,
    video_id: int
):
    result = await db.execute(
        select(Video).where(Video.id == video_id)
    )
    video = result.scalar_one_or_none()

    if not video:
        return False

    await db.delete(video)
    await db.commit()
    return True

async def create_frame(
    db: AsyncSession,
    video_id: int,
    frame_number: int,
    frame_path: str
):
    frame = Frame(
        video_id=video_id,
        frame_number=frame_number,
        frame_path=frame_path
    )
    db.add(frame)
    await db.commit()
    await db.refresh(frame)
    return frame

async def get_frame_by_id(
    db: AsyncSession,
    frame_id: int
):
    result = await db.execute(
        select(Frame)
        .where(Frame.id == frame_id)
        .options(selectinload(Frame.inference_results))
    )
    return result.scalar_one_or_none()

async def update_frame(
    db: AsyncSession,
    frame_id: int,
    frame_number: Optional[int] = None,
    frame_path: Optional[str] = None
):
    result = await db.execute(
        select(Frame).where(Frame.id == frame_id)
    )
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

async def delete_frame(
    db: AsyncSession,
    frame_id: int
):
    result = await db.execute(
        select(Frame).where(Frame.id == frame_id)
    )
    frame = result.scalar_one_or_none()

    if not frame:
        return False

    await db.delete(frame)
    await db.commit()
    return True

async def create_inference(
    db: AsyncSession,
    frame_id: int,
    class_name: str,
    confidence: float,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    polygon: Optional[List[float]] = None
):
    inference = Inference(
        frame_id=frame_id,
        class_name=class_name,
        confidence=confidence,
        x_min=x_min,
        y_min=y_min,
        x_max=x_max,
        y_max=y_max,
        polygon=polygon
    )

    db.add(inference)
    await db.commit()
    await db.refresh(inference)
    return inference

async def get_inference_by_id(
    db: AsyncSession,
    inference_id: int
):
    result = await db.execute(
        select(Inference)
        .where(Inference.id == inference_id)
    )
    return result.scalar_one_or_none()

async def update_inference(
    db: AsyncSession,
    inference_id: int,
    **kwargs
):
    result = await db.execute(
        select(Inference).where(Inference.id == inference_id)
    )
    inference = result.scalar_one_or_none()

    if not inference:
        return None

    for key, value in kwargs.items():
        if hasattr(inference, key) and value is not None:
            setattr(inference, key, value)

    await db.commit()
    await db.refresh(inference)
    return inference

async def delete_inference(
    db: AsyncSession,
    inference_id: int
):
    result = await db.execute(
        select(Inference).where(Inference.id == inference_id)
    )
    inference = result.scalar_one_or_none()

    if not inference:
        return False

    await db.delete(inference)
    await db.commit()
    return True