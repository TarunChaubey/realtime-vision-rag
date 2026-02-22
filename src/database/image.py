from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.image import Image, ImageInferenceResult


async def create_image(db: AsyncSession, file_name: str, file_path: str) -> Image:
    image = Image(file_name=file_name, file_path=file_path)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image_by_id(db: AsyncSession, image_id: int) -> Optional[Image]:
    result = await db.execute(
        select(Image).where(Image.id == image_id)
        .options(selectinload(Image.inference_results))
    )
    return result.scalar_one_or_none()


async def get_all_images(db: AsyncSession) -> list[Image]:
    result = await db.execute(select(Image))
    return result.scalars().all()


async def delete_image(db: AsyncSession, image_id: int) -> bool:
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if not image:
        return False
    await db.delete(image)
    await db.commit()
    return True
