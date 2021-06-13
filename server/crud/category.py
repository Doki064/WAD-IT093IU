from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Category
from schemas import CategoryCreate


async def create(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_by_uid(db: Session, category_uid: int) -> Category:
    q = select(Category).where(Category.uid == category_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> Category:
    q = select(Category).where(Category.name == name)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[Category]:
    q = select(Category)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
