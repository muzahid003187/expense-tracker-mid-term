import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

base = declarative_base()


def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()