"""All transaction API methods."""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_database
from schemas import TransactDetail, Transaction
from crud import transaction as _transaction
from crud import transact_detail as _transact_detail

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/{transaction_uid}", response_model=Transaction)
def read_transaction(transaction_uid: int, db: Session = Depends(get_database)):
    db_transaction = _transaction.get_by_uid(db, transaction_uid=transaction_uid)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Importation not found")
    return db_transaction


@router.get("/{date}", response_model=List[Transaction])
def read_transactions_by_date(date: datetime,
                              limit: int = 100,
                              db: Session = Depends(get_database)):
    db_transaction = _transaction.get_by_date(db, date=date, limit=limit)
    return db_transaction


@router.get("/", response_model=List[Transaction])
def read_transactions(skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(get_database)):
    return _transaction.get_all(db, skip=skip, limit=limit)


@router.get("/{transaction_uid}/details/", response_model=List[TransactDetail])
def read_customer_transactions(transaction_uid: int, db: Session = Depends(get_database)):
    db_transaction_details = _transact_detail.get_by_importation(
        db, transaction_uid=transaction_uid)
    return db_transaction_details
