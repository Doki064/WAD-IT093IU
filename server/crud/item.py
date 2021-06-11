from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Item
from schemas import ItemCreate


async def create(db: Session, item: ItemCreate, category_uid: int, shop_uid: int) -> Item:
    db_item = Item(**item.dict(), category_uid=category_uid, shop_uid=shop_uid)
    db.add(db_item)
    await db.commit()
    return db_item


async def get_by_uid(db: Session, item_uid: int) -> Item:
    q = select(Item).where(Item.uid == item_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> Item:
    q = select(Item).where(Item.name == name)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    q = select(Item).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
