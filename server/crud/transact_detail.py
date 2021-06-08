from sqlalchemy.orm import Session

from models import TransactDetail
from schemas import TransactDetailCreate


def create(db: Session, transaction_detail: TransactDetailCreate, transaction_uid: int,
           item_uid: int):
    db_transaction_detail = TransactDetail(**transaction_detail.dict(),
                                           transaction_uid=transaction_uid,
                                           item_uid=item_uid)
    db.add(db_transaction_detail)
    db.commit()
    db.refresh(db_transaction_detail)
    return db_transaction_detail


def get_by_transaction(db: Session, transaction_uid: int):
    return db.query(TransactDetail).filter(
        TransactDetail.transaction_uid == transaction_uid).limit(100).all()
