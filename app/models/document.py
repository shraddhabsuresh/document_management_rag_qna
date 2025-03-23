from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from app.database import Base  # Import Base from database.py

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(JSONB, nullable=True)  # Store embeddings as JSONB
