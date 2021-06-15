"""All customer route methods."""
from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, Body

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


@router.post("/", response_model=Customer, status_code=201)
async def create_customer(customer: CustomerCreate):
    async with async_session() as session:
        async with session.begin():
            db_customer = await _customer.get_by_name(session, name=customer.name)
            if db_customer is not None:
                raise HTTPException(status_code=409, detail="Customer already exists")
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


@router.get("/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int):
    async with async_session() as session:
        async with session.begin():
            db_customer = await _customer.get_by_id(session, customer_id=customer_id)
            if db_customer is None:
                raise HTTPException(status_code=404, detail="Customer not found")
            return db_customer


@router.post("/{customer_id}/transactions/", response_model=Transaction, status_code=201)
async def create_transaction_for_customer(customer_id: int,
                                          transaction: TransactionCreate,
                                          transaction_details: List[TransactDetailCreate],
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
                                                       customer_id=customer_id,
                                                       shop_id=db_shop.id)
            for detail in transaction_details:
                await _transact_detail.create(session,
                                              transaction_detail=detail,
                                              transaction_id=db_transaction.id,
                                              item_id=db_item.id)
            return db_transaction


@router.get("/{customer_id}/transactions/", response_model=List[Transaction])
async def read_transactions_of_customer(customer_id: int):
    async with async_session() as session:
        async with session.begin():
            db_customer = await _customer.get_by_id(session, customer_id=customer_id)
            if db_customer is None:
                raise HTTPException(status_code=404, detail="Customer not found")
            return db_customer.transactions
