from typing import List, Union, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Customer
from schemas import CustomerCreate


async def create(db: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    await db.commit()
    return db_customer


async def get_by_uid(db: Session, customer_uid: int) -> Union[Customer, None]:
    q = select(Customer).where(Customer.uid == customer_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_name(db: Session, name: str) -> Union[Customer, None]:
    q = select(Customer).where(Customer.name == name)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[Customer]:
    q = select(Customer)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
