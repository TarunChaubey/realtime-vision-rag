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

# Update with your database credentials
DATABASE_URL = "postgresql+psycopg2://postgres:postgrespassword@localhost:5432/ai_db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()