import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")