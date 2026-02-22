from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from src.models.base import Base
from src.core.config import settings

class Frame(Base):
    __tablename__ = "frames"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey(f"{settings.SCHEMA_NAME}.videos.id", ondelete="CASCADE"), nullable=False)
    frame_number = Column(Integer, nullable=False)
    frame_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    video = relationship("Video", back_populates="frames")
    inference_results = relationship(
        "InferenceResult", back_populates="frame",
        cascade="all, delete-orphan", passive_deletes=True
    )


class InferenceResult(Base):
    __tablename__ = "inference_results"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey(f"{settings.SCHEMA_NAME}.frames.id", ondelete="CASCADE"), nullable=False)
    class_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    x_min = Column(Float, nullable=False)
    y_min = Column(Float, nullable=False)
    x_max = Column(Float, nullable=False)
    y_max = Column(Float, nullable=False)
    polygon = Column(ARRAY(Float), nullable=True, default=None)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    frame = relationship("Frame", back_populates="inference_results")
