import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure engine with proper connection pooling and timeout handling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # Number of connections to maintain in pool
    max_overflow=20,  # Additional connections beyond pool_size
    pool_pre_ping=True,  # Test connections before use (prevents stale connections)
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=30,  # Timeout when getting connection from pool
    echo=False,  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
