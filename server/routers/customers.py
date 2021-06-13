"""All customer route methods."""
from typing import List, Union, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Body

from database.config import async_session
from schemas import (
    Customer,
    CustomerCreate,
    TransactDetailCreate,
    Transaction,
    TransactionCreate,
)
from crud import customer as _customer
from crud import shop as _shop
from crud import item as _item
from crud import transact_detail as _transact_detail
from crud import transaction as _transaction

router = APIRouter(
    prefix="/api/customers",
    tags=["customers"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    async with async_session() as session:
        async with session.begin():
            db_customer = await _customer.get_by_name(session, name=customer.name)
            if db_customer is not None:
                raise HTTPException(status_code=400, detail="Customer already exists")
            return await _customer.create(session, customer=customer)


@router.get("/", response_model=Union[Customer, List[Customer]])
async def read_customers(customer_name: Optional[str] = None,
                         skip: Optional[int] = None,
                         limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            if customer_name is not None:
                db_customer = await _customer.get_by_name(session, name=customer_name)
                if db_customer is None:
                    raise HTTPException(status_code=404, detail="Customer not found")
                return db_customer
            return await _customer.get_all(session, skip=skip, limit=limit)


@router.get("/{customer_uid}", response_model=Customer)
async def read_customer(customer_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_customer = await _customer.get_by_uid(session, customer_uid=customer_uid)
            if db_customer is None:
                raise HTTPException(status_code=404, detail="Customer not found")
            return db_customer


@router.post("/{customer_uid}/transactions/", response_model=Transaction)
async def create_transaction_for_customer(customer_uid: int,
                                          transaction: TransactionCreate,
                                          transaction_details: List[TransactDetailCreate],
                                          background_tasks: BackgroundTasks,
                                          item_name: str = Body(...),
                                          shop_name: str = Body(...)):
    async with async_session() as session:
        async with session.begin():
            db_item = await _item.get_by_name(session, item_name)
            if db_item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            db_shop = await _shop.get_by_name(session, shop_name)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            db_transaction = await _transaction.create(session,
                                                       transaction=transaction,
                                                       customer_uid=customer_uid,
                                                       shop_uid=db_shop.uid)
            # for detail in transaction_details:
            #     await _transact_detail.create(session,
            #                                   transaction_detail=detail,
            #                                   transaction_uid=db_transaction.uid,
            #                                   item_uid=db_item.uid)
            background_tasks.add_task(_create_transaction_details, session,
                                      transaction_details, db_transaction.uid,
                                      db_item.uid)
            return db_transaction


@router.get("/{customer_uid}/transactions/", response_model=List[Transaction])
async def read_transactions_of_customer(customer_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_customer = await _customer.get_by_uid(session, customer_uid=customer_uid)
            if db_customer is None:
                raise HTTPException(status_code=404, detail="Customer not found")
            return db_customer.transactions


async def _create_transaction_details(session,
                                      transaction_details: List[TransactDetailCreate],
                                      transaction_uid: int, item_uid: int):
    for detail in transaction_details:
        await _transact_detail.create(session,
                                      transaction_detail=detail,
                                      transaction_uid=transaction_uid,
                                      item_uid=item_uid)
