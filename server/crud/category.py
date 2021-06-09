from sqlalchemy.orm import Session

from models import Category
from schemas import CategoryCreate


def create(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_by_uid(db: Session, category_uid: int):
    return db.query(Category).filter(Category.uid == category_uid).first()


def get_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name.like(f"%{name}%")).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()
