"""Sets up the SQLAlchemy engine, session factory, and a get_db() dependency that FastAPI injects into routes.
 This is the only file that knows how the app connects to Postgres"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,       # Prevents automatic flushing before queries
    expire_on_commit=False) # Keeps data accessible on objects after commitsss


def get_session():
    """creates a new database session for each request and closes it when the request is done"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



