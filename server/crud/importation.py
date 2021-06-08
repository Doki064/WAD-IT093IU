from datetime import datetime

from sqlalchemy.sql import functions
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


def get_by_date(db: Session, date: datetime):
    return db.query(Importation).filter(Importation.date == date).limit(100).all()


def get_by_shop(db: Session, shop_uid: int):
    return (
        db.query(Importation).filter(Importation.shop_uid == shop_uid).limit(100).all()
    )


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Importation).offset(skip).limit(limit).all()


def get_min_date(db: Session):
    return db.query(Importation).filter(functions.min(Importation.date)).first().date


def get_max_date(db: Session):
    return db.query(Importation).filter(functions.max(Importation.date)).first().date


# def max_id(connection):
#     cur = connection.cursor()
#     cur.execute("""SELECT MAX (importID) FROM Imports""")
#     _id = None
#     try:
#         _id = cur.fetchone()[0]
#     except TypeError:
#         pass
#     return _id
