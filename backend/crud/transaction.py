from typing import List, Union
from datetime import date

from sqlalchemy.future import select
from sqlalchemy.orm import Session, subqueryload

from models import Transaction
from schemas import TransactionCreate


async def create(
    db: Session, transaction: TransactionCreate, customer_id: int, shop_id: int
) -> Transaction:
    db_transaction = Transaction(
        **transaction.dict(), customer_id=customer_id, shop_id=shop_id
    )
    db.add(db_transaction)
    await db.commit()
    return db_transaction


async def get_by_id(db: Session, transaction_id: int) -> Union[Transaction, None]:
    q = select(Transaction).where(Transaction.id == transaction_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_date(db: Session, date: date, limit: int) -> List[Transaction]:
    q = select(Transaction).limit(limit).where(Transaction.date == date)
    result = await db.execute(q)
    return result.scalars().all()


async def get_by_status(db: Session, status: str, limit: int) -> List[Transaction]:
    q = select(Transaction).limit(limit).where(Transaction.status == status)
    result = await db.execute(q)
    return result.scalars().all()


async def get_all(db: Session, skip: int, limit: int) -> List[Transaction]:
    q = select(Transaction).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def get_min_date(db: Session) -> Union[date, None]:
    q = select(Transaction.date).order_by(Transaction.date.asc())
    result = await db.execute(q)
    min_date = result.scalar()
    if min_date is None:
        return None
    return min_date


async def get_max_date(db: Session) -> Union[date, None]:
    q = select(Transaction.date).order_by(Transaction.date.desc())
    result = await db.execute(q)
    max_date = result.scalar()
    if max_date is None:
        return None
    return max_date


async def get_statistics(db: Session, skip: int, limit: int) -> List[Transaction]:
    q = select(Transaction).options(subqueryload(Transaction.transaction_details)) \
        .offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
