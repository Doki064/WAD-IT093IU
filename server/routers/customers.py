"""All customer API methods."""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_database
import crud.customer as crud
from schemas import Customer, CustomerCreate

router = APIRouter(
    prefix="/api/customers",
    tags=["customers"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_database)):
    db_customer = crud.get_by_name(db, name=customer.name)
    if db_customer is not None:
        raise HTTPException(status_code=400, detail="Customer already added")
    return crud.create(db, customer=customer)


@router.get("/", response_model=Customer)
def read_customer(customer_uid: Optional[int] = None,
                  customer_name: Optional[str] = None,
                  db: Session = Depends(get_database)):
    db_customer = None
    if customer_uid is not None:
        db_customer = crud.get_by_uid()(db, customer_uid=customer_uid)
    elif customer_name is not None:
        db_customer = crud.get_by_name(db, name=customer_name)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.get("/all/", response_model=List[Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return crud.get_all(db, skip=skip, limit=limit)
