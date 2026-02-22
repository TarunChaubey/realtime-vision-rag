import os
import uuid
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.core.database import get_db
from src.database.image import create_image, get_image_by_id, get_all_images, delete_image

router = APIRouter(prefix="/images", tags=["Images"])

ALLOWED = {".jpg", ".jpeg", ".png"}
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(status_code=400, detail="Only .jpg, .jpeg, .png allowed")
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return await create_image(db, file_name=file.filename, file_path=file_path)


@router.get("/")
async def list_images(db: AsyncSession = Depends(get_db)):
    return await get_all_images(db)


@router.get("/{image_id}")
async def get_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.delete("/{image_id}")
async def delete_image_endpoint(image_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_image(db, image_id):
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}
