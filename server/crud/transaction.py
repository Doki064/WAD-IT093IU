from typing import List, Union
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Transaction
from schemas import TransactionCreate


async def create(db: Session, transaction: TransactionCreate, customer_uid: int,
                 shop_uid: int) -> Transaction:
    db_transaction = Transaction(**transaction.dict(),
                                 customer_uid=customer_uid,
                                 shop_uid=shop_uid)
    db.add(db_transaction)
    await db.commit()
    return db_transaction


async def get_by_uid(db: Session, transaction_uid: int) -> Transaction:
    q = select(Transaction).where(Transaction.uid == transaction_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_date(db: Session, date: datetime, limit: int = 100) -> List[Transaction]:
    # return db.query(Transaction).filter(
    q = select(Transaction).limit(limit).where(
        Transaction.date == datetime.strftime(date))
    result = await db.execute(q)
    return result.scalars().all()


async def get_by_status(db: Session, status: str, limit: int = 100) -> List[Transaction]:
    q = select(Transaction).limit(limit).where(Transaction.status == status)
    result = await db.execute(q)
    return result.scalars().all()


async def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Transaction]:
    q = select(Transaction).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def get_min_date(db: Session) -> Union[datetime, None]:
    q = select(Transaction.date).order_by(Transaction.date.asc())
    result = await db.execute(q)
    date = result.scalar()
    if date is None:
        return None
    date = datetime.strptime(str(date), "%Y-%m-%d")
    return date


async def get_max_date(db: Session) -> Union[datetime, None]:
    q = select(Transaction.date).order_by(Transaction.date.desc())
    result = await db.execute(q)
    date = result.scalar()
    if date is None:
        return None
    date = datetime.strptime(str(date), "%Y-%m-%d")
    return date
