from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import ImportDetail
from schemas import ImportationCreate


async def create(
    db: Session, importation_detail: ImportationCreate, importation_id: int, item_id: int
) -> ImportDetail:
    db_importation_detail = ImportDetail(
        **importation_detail.dict(), importation_id=importation_id, item_id=item_id
    )
    db.add(db_importation_detail)
    await db.commit()
    return db_importation_detail


async def get_all(db: Session, skip: int, limit: int) -> List[ImportDetail]:
    q = select(ImportDetail).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def get_importation_details(db: Session, importation_id: int) -> List[ImportDetail]:
    q = select(ImportDetail).where(ImportDetail.importation_id == importation_id)
    result = await db.execute(q)
    return result.scalars().all()
