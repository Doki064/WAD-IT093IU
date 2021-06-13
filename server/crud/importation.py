from typing import List, Union, Optional
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Importation
from schemas import ImportationCreate


async def create(db: Session, importation: ImportationCreate,
                 shop_uid: int) -> Importation:
    db_importation = Importation(**importation.dict(), shop_uid=shop_uid)
    db.add(db_importation)
    await db.commit()
    await db.refresh(db_importation)
    return db_importation


async def get_by_uid(db: Session, importation_uid: int) -> Importation:
    q = select(Importation).where(Importation.uid == importation_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_date(db: Session,
                      date: datetime,
                      limit: Optional[int] = None) -> List[Importation]:
    q = select(Importation).where(Importation.date == datetime.strftime(date))
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


async def get_min_date(db: Session) -> Union[datetime, None]:
    q = select(Importation.date).order_by(Importation.date.asc())
    result = await db.execute(q)
    date = result.scalar()
    if date is None:
        return None
    date = datetime.strptime(str(date), "%Y-%m-%d")
    return date


async def get_max_date(db: Session) -> Union[datetime, None]:
    q = select(Importation.date).order_by(Importation.date.desc())
    result = await db.execute(q)
    date = result.scalar()
    if date is None:
        return None
    date = datetime.strptime(str(date), "%Y-%m-%d")
    return date
