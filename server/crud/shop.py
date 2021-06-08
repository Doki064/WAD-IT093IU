from sqlalchemy.orm import Session

from models import Shop
from schemas import ShopCreate


def create(db: Session, shop: ShopCreate):
    db_shop = Shop(name=shop.name)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def get_by_uid(db: Session, shop_uid: int):
    return db.query(Shop).filter(Shop.uid == shop_uid).first()


def get_by_name(db: Session, name: str):
    return db.query(Shop).filter(Shop.name.like(f"%{name}%")).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Shop).offset(skip).limit(limit).all()


# def delete_by_id(connection, shop_id):
#     cur = connection.cursor()
#     cur.execute('''DELETE FROM Shop WHERE shopID = ?''', (shop_id,))
#     connection.commit()

# def max_id(connection):
#     cur = connection.cursor()
#     cur.execute('''SELECT MAX (shopID) FROM Shop''')
#     _id = None
#     try:
#         _id = cur.fetchone()[0]
#     except TypeError:
#         pass
#     return _id
