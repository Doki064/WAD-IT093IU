from typing import List, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Shop
from schemas import ShopCreate


async def create(db: Session, shop: ShopCreate) -> Shop:
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    await db.commit()
    return db_shop


async def get_by_id(db: Session, shop_id: int) -> Union[Shop, None]:
    q = select(Shop).where(Shop.id == shop_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> Union[Shop, None]:
    q = select(Shop).where(Shop.name == name)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session, skip: int, limit: int) -> List[Shop]:
    q = select(Shop).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
