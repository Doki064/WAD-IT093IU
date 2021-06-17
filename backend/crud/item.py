from typing import List, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Item
from schemas import ItemCreate


async def create(db: Session, item: ItemCreate, category_id: int, shop_id: int) -> Item:
    db_item = Item(**item.dict(), category_id=category_id, shop_id=shop_id)
    db.add(db_item)
    await db.commit()
    return db_item


async def get_by_id(db: Session, item_id: int) -> Union[Item, None]:
    q = select(Item).where(Item.id == item_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> Union[Item, None]:
    q = select(Item).where(Item.name == name)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session, skip: int, limit: int) -> List[Item]:
    q = select(Item).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
