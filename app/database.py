from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if used)
load_dotenv()

# PostgreSQL Database URL (Change as per your configuration)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/document_db")

# Create Engine
engine = create_engine(DATABASE_URL)

# Create Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
