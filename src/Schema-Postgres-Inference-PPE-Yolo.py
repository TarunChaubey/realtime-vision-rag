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

schema_name = "videos_inference"

# Update with your database credentials
DATABASE_URL = "postgresql+psycopg2://postgres:postgrespassword@localhost:5432/ai_db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

schema_name = "video_inference"

# Define Table Models
class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {"schema": schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
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


# Ensure schema exists (important for PostgreSQL)
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
    conn.commit()

# Create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
# Example Insert Workflow
with Session() as session:
    video = Video(file_path="../Data/Videos/dust.mp4")
    frame = Frame(frame_number=1, frame_path="frames/sample_frame_1.jpg")

    video.frames.append(frame)

    session.add(video)
    session.commit()

    frame_id = frame.id
