import os
import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

BASE_DIR = Path(__file__).absolute().parents[1]
load_dotenv(BASE_DIR.joinpath(".env"))

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
