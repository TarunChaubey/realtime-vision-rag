from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    TIMESTAMP,
    text,
    func,
    DateTime
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import ARRAY

schema_name = "video_inference"
Base = declarative_base()

# Define Table Models
class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    frames = relationship(
        "Frame",
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Frame(Base):
    __tablename__ = "frames"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(
        Integer,
        ForeignKey(f"{schema_name}.videos.id", ondelete="CASCADE"),
        nullable=False
    )
    frame_number = Column(Integer, nullable=False)
    frame_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    video = relationship("Video", back_populates="frames")

    inference_results = relationship(
        "Inference",
        back_populates="frame",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Inference(Base):
    __tablename__ = "inference_results"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(
        Integer,
        ForeignKey(f"{schema_name}.frames.id", ondelete="CASCADE"),
        nullable=False
    )

    class_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)

    # Bounding Box
    x_min = Column(Float, nullable=False)
    y_min = Column(Float, nullable=False)
    x_max = Column(Float, nullable=False)
    y_max = Column(Float, nullable=False)

    # New: List of keypoints (coordinates)
    polygon = Column(ARRAY(Float), nullable=True, default=None)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    frame = relationship("Frame", back_populates="inference_results")