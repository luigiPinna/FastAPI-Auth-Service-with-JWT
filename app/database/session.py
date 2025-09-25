from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings

# Engine PostgreSQL con configurazione standard
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log delle query SQL solo in debug
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Dependency injection. Crea una sessione DB, la yielda, poi la chiude automaticamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()