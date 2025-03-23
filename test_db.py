from app.core.database import get_db
import asyncio
from sqlalchemy import text

async def test_db():
    async for session in get_db():
        try:
            # result = await session.execute("SELECT 1")
            result = await session.execute(text("SELECT 1"))

            print("Database is connected:", result.fetchone())
        except Exception as e:
            print("Database connection failed:", e)

asyncio.run(test_db())
