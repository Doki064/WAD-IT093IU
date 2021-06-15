from typing import List, Union, Optional
from datetime import date

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Importation
from schemas import ImportationCreate


async def create(db: Session, importation: ImportationCreate,
                 shop_id: int) -> Importation:
    db_importation = Importation(**importation.dict(), shop_id=shop_id)
    db.add(db_importation)
    await db.commit()
    return db_importation


async def get_by_id(db: Session, importation_id: int) -> Union[Importation, None]:
    q = select(Importation).where(Importation.id == importation_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_date(db: Session,
                      date: date,
                      limit: Optional[int] = None) -> List[Importation]:
    q = select(Importation).where(Importation.date == date)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[Importation]:
    q = select(Importation)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def get_min_date(db: Session) -> Union[date, None]:
    q = select(Importation.date).order_by(Importation.date.asc())
    result = await db.execute(q)
    min_date = result.scalar()
    if min_date is None:
        return None
    return min_date


async def get_max_date(db: Session) -> Union[date, None]:
    q = select(Importation.date).order_by(Importation.date.desc())
    result = await db.execute(q)
    max_date = result.scalar()
    if max_date is None:
        return None
    return max_date
