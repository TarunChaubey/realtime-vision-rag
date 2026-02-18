
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
    DateTime,
    TEXT,
    Text
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import ARRAY

# Schema for multi-modal embeddings
schema_name = "multi_modal_rag"
Base = declarative_base()

# Source Dataset Table
class Source(Base):
    __tablename__ = "sources"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)  # e.g., "text", "image", "audio", "video"
    file_path = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    embeddings = relationship(
        "Embedding",
        back_populates="source",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# Embedding Table
class Embedding(Base):
    __tablename__ = "embeddings"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(
        Integer,
        ForeignKey(f"{schema_name}.sources.id", ondelete="CASCADE"),
        nullable=False
    )
    modality = Column(String, nullable=False)  # "text", "image", "audio"
    embedding_vector = Column(ARRAY(Float), nullable=False)  # vector embeddings
    embedding_metadata = Column(Text, nullable=True)  # renamed from 'metadata'
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    source = relationship("Source", back_populates="embeddings")

# Optional: Text-specific metadata
class TextMetadata(Base):
    __tablename__ = "text_metadata"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(
        Integer,
        ForeignKey(f"{schema_name}.sources.id", ondelete="CASCADE"),
        nullable=False
    )
    language = Column(String, nullable=True)
    word_count = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

# Optional: Image-specific metadata
class ImageMetadata(Base):
    __tablename__ = "image_metadata"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(
        Integer,
        ForeignKey(f"{schema_name}.sources.id", ondelete="CASCADE"),
        nullable=False
    )
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    format = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

# Optional: Audio-specific metadata
class AudioMetadata(Base):
    __tablename__ = "audio_metadata"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(
        Integer,
        ForeignKey(f"{schema_name}.sources.id", ondelete="CASCADE"),
        nullable=False
    )
    duration_seconds = Column(Float, nullable=True)
    sample_rate = Column(Integer, nullable=True)
    channels = Column(Integer, nullable=True)
    format = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)