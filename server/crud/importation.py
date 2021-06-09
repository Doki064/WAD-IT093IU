from datetime import datetime

from sqlalchemy.orm import Session

from models import Importation
from schemas import ImportationCreate


def create(db: Session, importation: ImportationCreate, shop_uid: int):
    db_importation = Importation(**importation.dict(), shop_uid=shop_uid)
    db.add(db_importation)
    db.commit()
    db.refresh(db_importation)
    return db_importation


def get_by_uid(db: Session, importation_uid: int):
    return db.query(Importation).filter(Importation.uid == importation_uid).first()


def get_by_date(db: Session, date: datetime, limit: int = 100):
    return db.query(Importation).filter(
        Importation.date == datetime.strftime(date)).limit(limit).all()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Importation).offset(skip).limit(limit).all()


def get_min_date(db: Session):
    date = db.query(Importation.date).order_by(Importation.date.asc()).scalar()
    if date is None:
        return None
    date = datetime.strptime(str(date), "%Y-%m-%d")
    return date


def get_max_date(db: Session):
    date = db.query(Importation.date).order_by(Importation.date.desc()).scalar()
    if date is None:
        return None
    date = datetime.strptime(str(date), "%Y-%m-%d")
    return date
