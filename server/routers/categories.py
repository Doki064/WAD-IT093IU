"""All category API methods."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_database
import crud.category as crud
from schemas import Category, CategoryCreate, Item

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_database)):
    db_category = crud.get_by_name(db, name=category.name)
    if db_category is not None:
        raise HTTPException(status_code=400, detail="Category already added")
    return crud.create(db, category=category)


@router.get("/{category_uid}", response_model=Category)
def read_category(category_uid: int, db: Session = Depends(get_database)):
    db_category = crud.get_by_uid(db, category_uid=category_uid)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/{category_name}", response_model=Category)
def read_category_by_name(category_name: str, db: Session = Depends(get_database)):
    db_category = crud.get_by_name(db, name=category_name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return crud.get_all(db, skip=skip, limit=limit)


@router.get("/{category_uid}/items/", response_model=List[Item])
def read_category_items(category_uid: int, db: Session = Depends(get_database)):
    db_category = crud.get_by_uid(db, category_uid=category_uid)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category.items
