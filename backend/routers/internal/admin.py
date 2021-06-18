"""All internal API methods for admin only."""
from typing import Dict, List

import pandas as pd
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse

import models
from schemas import Transaction, TransactDetail
from routers.internal import APIRouter
from database.config import async_session
from crud import transaction as _transaction
from crud import transact_detail as _transact_detail

router = APIRouter(
    prefix="/internal/admin",
    tags=["admin"],
    responses={418: {
        "description": "I'm a teapot"
    }},
)


@router.get("")
def read_table_info() -> Dict[str, List[str]]:
    response = dict()
    for model in models.__all__:
        key = getattr(models, model).__tablename__
        value = getattr(models, model).__table__.c.keys()
        response[key] = value
    return response


@router.get("/plot")
async def read_transaction_plot(skip: int = 0, limit: int = 1000000):
    async with async_session() as session:
        async with session.begin():
            db_transactions = await _transaction.get_all(session, skip=skip, limit=limit)
            transactions = [
                dict(Transaction.from_orm(transaction)) for transaction in db_transactions
            ]
            transactions_df = pd.DataFrame.from_records(transactions)
            db_details = await _transact_detail.get_all(session, skip=skip, limit=limit)
            details = [dict(TransactDetail.from_orm(detail)) for detail in db_details]
            details_df = pd.DataFrame.from_records(details)
            df = pd.merge(
                transactions_df, details_df, left_on="id", right_on="transaction_id"
            )
            df = df.drop(["id", "status", "transaction_id"], axis=1)
            return PlainTextResponse(df.to_csv(index=False), media_type="text/csv")


@router.get("/table")
async def read_table_statistics():
    raise HTTPException(status_code=501)
