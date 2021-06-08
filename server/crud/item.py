from sqlalchemy.orm import Session

from models import Item
from schemas import ItemCreate


def create(db: Session, item: ItemCreate, category_uid: int, shop_uid: int):
    db_item = Item(**item.dict(), category_uid=category_uid, shop_uid=shop_uid)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_by_uid(db: Session, item_uid: int):
    return db.query(Item).filter(Item.uid == item_uid).first()


def get_by_name(db: Session, name: str):
    return db.query(Item).filter(Item.name.like(f"%{name}%")).first()


def get_by_category(db: Session, category_uid: int):
    return db.query(Item).filter(
        Item.category_uid == category_uid).limit(100).all()


def get_by_shop(db: Session, shop_uid: int):
    return db.query(Item).filter(Item.shop_uid == shop_uid).limit(100).all()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


# def delete_by_id(connection, item_id):
#     cur = connection.cursor()
#     cur.execute("""DELETE FROM Item WHERE itemID = ?""", (item_id,))
#     connection.commit()

# def max_id(connection):
#     cur = connection.cursor()
#     cur.execute("""SELECT MAX (itemID) FROM Item""")
#     _id = None
#     try:
#         _id = cur.fetchone()[0]
#     except TypeError:
#         pass
#     return _id
