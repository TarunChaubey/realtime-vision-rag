from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from src.models.base import Base

RAG_SCHEMA = "multi_modal_rag"

class Source(Base):
    __tablename__ = "sources"
    __table_args__ = {"schema": RAG_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    embeddings = relationship(
        "Embedding", back_populates="source",
        cascade="all, delete-orphan", passive_deletes=True
    )


class Embedding(Base):
    __tablename__ = "embeddings"
    __table_args__ = {"schema": RAG_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey(f"{RAG_SCHEMA}.sources.id", ondelete="CASCADE"), nullable=False)
    modality = Column(String, nullable=False)
    embedding_vector = Column(ARRAY(Float), nullable=False)
    embedding_metadata = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    source = relationship("Source", back_populates="embeddings")
