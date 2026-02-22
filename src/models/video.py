from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.core.config import settings

class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    frames = relationship(
        "Frame", back_populates="video",
        cascade="all, delete-orphan", passive_deletes=True
    )
