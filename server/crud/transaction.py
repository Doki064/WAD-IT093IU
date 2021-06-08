from datetime import datetime

from sqlalchemy.sql import functions
from sqlalchemy.orm import Session

from models import Transaction
from schemas import TransactionCreate


def create(
    db: Session, transaction: TransactionCreate, customer_uid: int, shop_uid: int
):
    db_transaction = Transaction(
        **transaction.dict(), customer_uid=customer_uid, shop_uid=shop_uid
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_by_uid(db: Session, transaction_uid: int):
    return db.query(Transaction).filter(Transaction.uid == transaction_uid).first()


def get_by_date(db: Session, date: datetime):
    return db.query(Transaction).filter(Transaction.date == date).limit(100).all()


def get_by_status(db: Session, status: str):
    return db.query(Transaction).filter(Transaction.status == status).limit(100).all()


def get_by_customer(db: Session, customer_uid: int):
    return (
        db.query(Transaction)
        .filter(Transaction.customer_uid == customer_uid)
        .limit(100)
        .all()
    )


def get_by_shop(db: Session, shop_uid: int):
    return (
        db.query(Transaction).filter(Transaction.shop_uid == shop_uid).limit(100).all()
    )


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()


def get_min_date(db: Session):
    return db.query(Transaction).filter(functions.min(Transaction.date)).first().date


def get_max_date(db: Session):
    return db.query(Transaction).filter(functions.max(Transaction.date)).first().date


# def max_id(connection):
#     cur = connection.cursor()
#     cur.execute("""SELECT MAX (transactionID) FROM Transactions""")
#     _id = None
#     try:
#         _id = cur.fetchone()[0]
#     except TypeError:
#         pass
#     return _id