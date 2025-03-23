[12:26 PM, 3/23/2025] Shraddha Suresh: import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector

# ✅ Load database URL from environment variable (or use default)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:Shraddha2014@localhost:5433/document_db")

# ✅ Create asynchronous database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ Create async session factory
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ✅ Define base class for models
Base = declarative_base()

# ✅ Document Model
class Document(Base):
    _tablename_ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # Ensure pgvector is installed ✅

# ✅ Dependency function to get a database session
async def get_db():
    async with async_session() as session:
        yield session    ----app>database.py code
[12:27 PM, 3/23/2025] Shraddha Suresh: from fastapi import FastAPI
from app.routes import api

app = FastAPI()

# Include the API router
app.include_router(api.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Document Management API"} -----app>main.py code
[12:28 PM, 3/23/2025] Shraddha Suresh: from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import your models
from model.document import Base  

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set metadata so Alembic knows about your tables
target_metadata = Base.metadata  

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

   