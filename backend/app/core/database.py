from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings
from app.core.logging import logger

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()

def init_db() -> None:
    """Initialize database tables."""
    from app.models import User, Document, Chunk, Extraction, Comparison, AgentRun, Report  # noqa
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully", extra={"extra_fields": {"url": settings.DATABASE_URL}})

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions with automatic commit/rollback."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session rollback due to error: {e}", exc_info=True)
        raise
    finally:
        session.close()

def get_db() -> Generator[Session, None, None]:
    """Dependency helper for route handlers."""
    with get_db_session() as session:
        yield session
