from typing import List, Union, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Shop
from schemas import ShopCreate


async def create(db: Session, shop: ShopCreate) -> Shop:
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    await db.commit()
    return db_shop


async def get_by_uid(db: Session, shop_uid: int) -> Union[Shop, None]:
    q = select(Shop).where(Shop.uid == shop_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> Union[Shop, None]:
    q = select(Shop).where(Shop.name == name)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[Shop]:
    q = select(Shop)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
