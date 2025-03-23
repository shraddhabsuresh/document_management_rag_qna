from sqlalchemy import text  # Import text from SQLAlchemy
from app.database import get_db

def test_retrieval():
    db = next(get_db())  # Get database session
    query = text("SELECT id, filename, embedding FROM documents")  # Wrap query in text()
    result = db.execute(query).fetchall()
    for row in result:
        print(row)

test_retrieval()
