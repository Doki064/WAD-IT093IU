from typing import List, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Category
from schemas import CategoryCreate


async def create(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    return db_category


async def get_by_id(db: Session, category_id: int) -> Union[Category, None]:
    q = select(Category).where(Category.id == category_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> List[Category]:
    q = select(Category).where(Category.ilike(f"%{name}%"))
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session, skip: int, limit: int) -> List[Category]:
    q = select(Category).where(Category.id > skip) \
        .order_by(Category.id).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
