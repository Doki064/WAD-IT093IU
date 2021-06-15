"""All transaction route methods."""
from typing import List, Optional
from datetime import date

from fastapi import HTTPException, Depends

from routers.internal import APIRouter
from core.security import auth
from database.config import async_session
from schemas import TransactDetail, Transaction
from crud import transaction as _transaction

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(auth.get_current_active_user)],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("", response_model=List[Transaction])
async def read_transactions(skip: Optional[int] = None, limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            return await _transaction.get_all(session, skip=skip, limit=limit)


@router.get("/date/{date}", response_model=List[Transaction])
async def read_transactions_by_date(date: date, limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            return await _transaction.get_by_date(session, date=date, limit=limit)


@router.get("/{transaction_id}", response_model=Transaction)
async def read_transaction(transaction_id: int):
    async with async_session() as session:
        async with session.begin():
            db_transaction = await _transaction.get_by_id(session,
                                                          transaction_id=transaction_id)
            if db_transaction is None:
                raise HTTPException(status_code=404, detail="Transaction not found")
            return db_transaction


@router.get("/{transaction_id}/details", response_model=List[TransactDetail])
async def read_transaction_details(transaction_id: int):
    async with async_session() as session:
        async with session.begin():
            db_transaction = await _transaction.get_by_id(session,
                                                          transaction_id=transaction_id)
            return db_transaction.transaction_details
