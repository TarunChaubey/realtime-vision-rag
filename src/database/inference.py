from typing import Optional, List, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.frame import InferenceFrame
from src.models.image import InferenceImage
from src.inference_pipeline.base import InferenceOutput


async def save_inference_output(
    db: AsyncSession,
    output: InferenceOutput,
    source_type: Literal["frame", "image"],
    source_id: int,
) -> list:
    saved = []
    for det in output.detections:
        if source_type == "frame":
            record = InferenceFrame(
                frame_id=source_id,
                class_name=det.class_name, confidence=det.confidence,
                x_min=det.x_min, y_min=det.y_min,
                x_max=det.x_max, y_max=det.y_max,
                polygon=det.polygon,
            )
        else:
            record = InferenceImage(
                image_id=source_id,
                class_name=det.class_name, confidence=det.confidence,
                x_min=det.x_min, y_min=det.y_min,
                x_max=det.x_max, y_max=det.y_max,
                polygon=det.polygon,
            )
        db.add(record)
        saved.append(record)
    await db.commit()
    for r in saved:
        await db.refresh(r)
    return saved


async def create_inference(
    db: AsyncSession, frame_id: int, class_name: str, confidence: float,
    x_min: float, y_min: float, x_max: float, y_max: float,
    polygon: Optional[List[float]] = None,
) -> InferenceFrame:
    record = InferenceFrame(
        frame_id=frame_id, class_name=class_name, confidence=confidence,
        x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max, polygon=polygon,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_inference_by_id(db: AsyncSession, inference_id: int) -> Optional[InferenceFrame]:
    result = await db.execute(select(InferenceFrame).where(InferenceFrame.id == inference_id))
    return result.scalar_one_or_none()


async def update_inference(db: AsyncSession, inference_id: int, **kwargs) -> Optional[InferenceFrame]:
    result = await db.execute(select(InferenceFrame).where(InferenceFrame.id == inference_id))
    inference = result.scalar_one_or_none()
    if not inference:
        return None
    for key, value in kwargs.items():
        if hasattr(inference, key) and value is not None:
            setattr(inference, key, value)
    await db.commit()
    await db.refresh(inference)
    return inference


async def delete_inference(db: AsyncSession, inference_id: int) -> bool:
    result = await db.execute(select(InferenceFrame).where(InferenceFrame.id == inference_id))
    inference = result.scalar_one_or_none()
    if not inference:
        return False
    await db.delete(inference)
    await db.commit()
    return True
