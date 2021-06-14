from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import TransactDetail
from schemas import TransactDetailCreate


async def create(db: Session, transaction_detail: TransactDetailCreate,
                 transaction_uid: int, item_uid: int) -> TransactDetail:
    db_transaction_detail = TransactDetail(**transaction_detail.dict(),
                                           transaction_uid=transaction_uid,
                                           item_uid=item_uid)
    db.add(db_transaction_detail)
    await db.commit()
    return db_transaction_detail


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[TransactDetail]:
    q = select(TransactDetail)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
