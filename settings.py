from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_DB = getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{DB_PASSWORD}@localhost:5432/{POSTGRES_DB}"
