"""All category API methods."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from database import get_database
from schemas import Category, CategoryCreate, Item, ItemCreate
from crud import category as _category
from crud import shop as _shop
from crud import item as _item

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_database)):
    db_category = _category.get_by_name(db, name=category.name)
    if db_category is not None:
        raise HTTPException(status_code=400, detail="Category already added")
    return _category.create(db, category=category)


@router.get("/{category_uid}", response_model=Category)
def read_category(category_uid: int, db: Session = Depends(get_database)):
    db_category = _category.get_by_uid(db, category_uid=category_uid)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/{category_name}", response_model=Category)
def read_category_by_name(category_name: str, db: Session = Depends(get_database)):
    db_category = _category.get_by_name(db, name=category_name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return _category.get_all(db, skip=skip, limit=limit)


@router.post("/{category_uid}/items/", response_model=Item)
def create_item(category_uid: int,
                item: ItemCreate,
                shop_name: str = Body(...),
                db: Session = Depends(get_database)):
    db_item = _item.get_by_name(db, name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already added")
    db_shop = _shop.get_by_name(db, name=shop_name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return _item.create(db, item=item, category_uid=category_uid, shop_uid=db_shop.uid)


@router.get("/{category_uid}/items/", response_model=List[Item])
def read_category_items(category_uid: int, db: Session = Depends(get_database)):
    db_category = _category.get_by_uid(db, category_uid=category_uid)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category.items
