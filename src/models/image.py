from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from src.models.base import Base
from src.core.config import settings


class Image(Base):
    __tablename__ = "images"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    inference_results = relationship(
        "ImageInferenceResult", back_populates="image",
        cascade="all, delete-orphan", passive_deletes=True
    )


class ImageInferenceResult(Base):
    __tablename__ = "image_inference_results"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(
        Integer,
        ForeignKey(f"{settings.SCHEMA_NAME}.images.id", ondelete="CASCADE"),
        nullable=False
    )
    class_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    x_min = Column(Float, nullable=False)
    y_min = Column(Float, nullable=False)
    x_max = Column(Float, nullable=False)
    y_max = Column(Float, nullable=False)
    polygon = Column(ARRAY(Float), nullable=True, default=None)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    image = relationship("Image", back_populates="inference_results")
