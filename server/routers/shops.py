"""All shop API methods."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_database
import crud.shop as crud
from schemas import Shop, ShopCreate, Item, Transaction, Importation

router = APIRouter(
    prefix="/api/shops",
    tags=["shops"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Shop)
def create_shop(shop: ShopCreate, db: Session = Depends(get_database)):
    db_shop = crud.get_by_name(db, name=shop.name)
    if db_shop is not None:
        raise HTTPException(status_code=400, detail="Shop already added")
    return crud.create(db, shop=shop)


@router.get("/{shop_uid}", response_model=Shop)
def read_shop(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = crud.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@router.get("/{shop_name}", response_model=Shop)
def read_shop_by_name(shop_name: str, db: Session = Depends(get_database)):
    db_shop = crud.get_by_name(db, name=shop_name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@router.get("/", response_model=List[Shop])
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return crud.get_all(db, skip=skip, limit=limit)


@router.get("/{shop_uid}/items/", response_model=List[Item])
def read_shop_items(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = crud.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop.items


@router.get("/{shop_uid}/transactions/", response_model=List[Transaction])
def read_shop_transactions(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = crud.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop.transactions


@router.get("/{shop_uid}/importations/", response_model=List[Importation])
def read_shop_importations(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = crud.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop.importations
