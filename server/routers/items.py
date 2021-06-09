"""All item API methods."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_database
import crud.item as crud
from schemas import Item, ItemCreate

router = APIRouter(
    prefix="/api/items",
    tags=["items"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Item)
def create_item(item: ItemCreate,
                category_uid: int,
                shop_uid: int,
                db: Session = Depends(get_database)):
    db_item = crud.get_by_name(db, name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already added")
    return crud.create(db, item=item, category_uid=category_uid, shop_uid=shop_uid)


@router.get("/{item_uid}", response_model=Item)
def read_item(item_uid: int, db: Session = Depends(get_database)):
    db_item = crud.get_by_uid(db, item_uid=item_uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/{item_name}", response_model=Item)
def read_item_by_name(item_name: str, db: Session = Depends(get_database)):
    db_item = crud.get_by_name(db, name=item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return crud.get_all(db, skip=skip, limit=limit)
