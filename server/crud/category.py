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


# def delete_by_id(connection, category_id):
#     cur = connection.cursor()
#     cur.execute('''DELETE FROM ItemCategory WHERE categoryID = ?''',
#                 (category_id,))
#     connection.commit()

# def max_id(connection):
#     cur = connection.cursor()
#     cur.execute('''SELECT MAX (categoryID) FROM ItemCategory''')
#     _id = None
#     try:
#         _id = cur.fetchone()[0]
#     except TypeError:
#         pass
#     return _id
