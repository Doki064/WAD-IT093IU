"""All shop API methods."""
from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from database import get_database
from schemas import (
    Shop,
    ShopCreate,
    Importation,
    ImportationCreate,
    ImportDetailCreate,
    Item,
    Transaction,
)
from crud import shop as _shop
from crud import item as _item
from crud import importation as _importation
from crud import import_detail as _import_detail

router = APIRouter(
    prefix="/api/shops",
    tags=["shops"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Shop)
def create_shop(shop: ShopCreate, db: Session = Depends(get_database)):
    db_shop = _shop.get_by_name(db, name=shop.name)
    if db_shop is not None:
        raise HTTPException(status_code=400, detail="Shop already added")
    return _shop.create(db, shop=shop)


@router.get("/", response_model=Union[Shop, List[Shop]])
def read_shops(shop_name: Optional[str] = None,
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_database)):
    if shop_name is not None:
        db_shop = _shop.get_by_name(db, name=shop_name)
        if db_shop is None:
            raise HTTPException(status_code=404, detail="Shop not found")
        return db_shop
    return _shop.get_all(db, skip=skip, limit=limit)


@router.get("/{shop_uid}", response_model=Shop)
def read_shop(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = _shop.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@router.post("/{shop_uid}/importations/", response_model=Importation)
def create_importation_for_shop(shop_uid: int,
                                importation: ImportationCreate,
                                importation_details: List[ImportDetailCreate],
                                item_name: str = Body(...),
                                db: Session = Depends(get_database)):
    db_item = _item.get_by_name(db, item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_importation = _importation.create(db, importation=importation, shop_uid=shop_uid)
    for detail in importation_details:
        _import_detail.create(db,
                              importation_detail=detail,
                              importation_uid=db_importation.uid,
                              item_uid=db_item.uid)
    return db_importation


@router.get("/{shop_uid}/importations/", response_model=List[Importation])
def read_shop_importations(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = _shop.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop.importations


@router.get("/{shop_uid}/transactions/", response_model=List[Transaction])
def read_shop_transactions(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = _shop.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop.transactions


@router.get("/{shop_uid}/items/", response_model=List[Item])
def read_shop_items(shop_uid: int, db: Session = Depends(get_database)):
    db_shop = _shop.get_by_uid(db, shop_uid=shop_uid)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop.items
