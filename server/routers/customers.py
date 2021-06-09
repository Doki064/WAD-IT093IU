"""All customer API methods."""
from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from database import get_database
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
def create_customer(customer: CustomerCreate, db: Session = Depends(get_database)):
    db_customer = _customer.get_by_name(db, name=customer.name)
    if db_customer is not None:
        raise HTTPException(status_code=400, detail="Customer already added")
    return _customer.create(db, customer=customer)


@router.get("/", response_model=Union[Customer, List[Customer]])
def read_customers(customer_name: Optional[str] = None,
                   skip: int = 0,
                   limit: int = 100,
                   db: Session = Depends(get_database)):
    if customer_name is not None:
        db_customer = _customer.get_by_name(db, name=customer_name)
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return db_customer
    return _customer.get_all(db, skip=skip, limit=limit)


@router.get("/{customer_uid}", response_model=Customer)
def read_customer(customer_uid: int, db: Session = Depends(get_database)):
    db_customer = _customer.get_by_uid(db, customer_uid=customer_uid)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.post("/{customer_uid}/transactions/", response_model=Transaction)
def create_transaction_for_customer(customer_uid: int,
                                    transaction: TransactionCreate,
                                    transaction_details: List[TransactDetailCreate],
                                    item_name: str = Body(...),
                                    shop_name: str = Body(...),
                                    db: Session = Depends(get_database)):
    db_item = _item.get_by_name(db, item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_shop = _shop.get_by_name(db, shop_name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    db_transaction = _transaction.create(db,
                                         transaction=transaction,
                                         customer_uid=customer_uid,
                                         shop_uid=db_shop.uid)
    for detail in transaction_details:
        _transact_detail.create(db,
                                transaction_detail=detail,
                                transaction_uid=db_transaction.uid,
                                item_uid=db_item.uid)
    return db_transaction


@router.get("/{customer_uid}/transactions/", response_model=List[Transaction])
def read_customer_transactions(customer_uid: int, db: Session = Depends(get_database)):
    db_customer = _customer.get_by_uid(db, customer_uid=customer_uid)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer.transactions
