from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import ImportDetail
from schemas import ImportationCreate


async def create(db: Session, importation_detail: ImportationCreate, importation_uid: int,
                 item_uid: int) -> ImportDetail:
    db_importation_detail = ImportDetail(**importation_detail.dict(),
                                         importation_uid=importation_uid,
                                         item_uid=item_uid)
    db.add(db_importation_detail)
    await db.commit()
    await db.refresh(db_importation_detail)
    return db_importation_detail


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[ImportDetail]:
    q = select(ImportDetail)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
