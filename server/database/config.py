import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./streamlit_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)
Base = declarative_base()


def create_database() -> None:
    Base.metadata.create_all(bind=engine)


def get_database():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        logger.exception('Session rollback because of exception')
        db.rollback()
        raise
    finally:
        db.close()
