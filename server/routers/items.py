"""All item API methods."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_database
from schemas import Item
from crud import item as _item

router = APIRouter(
    prefix="/api/items",
    tags=["items"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/{item_uid}", response_model=Item)
def read_item(item_uid: int, db: Session = Depends(get_database)):
    db_item = _item.get_by_uid(db, item_uid=item_uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/{item_name}", response_model=Item)
def read_item_by_name(item_name: str, db: Session = Depends(get_database)):
    db_item = _item.get_by_name(db, name=item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return _item.get_all(db, skip=skip, limit=limit)
