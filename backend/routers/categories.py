"""All category route methods."""
from typing import List, Union, Optional

from fastapi import HTTPException, Depends, Body

from routers.internal import APIRouter
from security import auth
from database.config import async_session
from schemas import Category, CategoryCreate, Item, ItemCreate
from crud import category as _category
from crud import shop as _shop
from crud import item as _item

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(auth.get_current_active_user)],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Category, status_code=201)
async def create_category(category: CategoryCreate):
    async with async_session() as session:
        async with session.begin():
            db_category = await _category.get_by_name(session, name=category.name)
            if db_category is not None:
                raise HTTPException(status_code=409, detail="Category already exists")
            return await _category.create(session, category=category)


@router.get("/", response_model=Union[Category, List[Category]])
async def read_categories(category_name: Optional[str] = None,
                          skip: Optional[int] = None,
                          limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            if category_name is not None:
                db_category = await _category.get_by_name(session, name=category_name)
                if db_category is None:
                    raise HTTPException(status_code=404, detail="Category not found")
                return db_category
            return await _category.get_all(session, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=Category)
async def read_category(category_id: int):
    async with async_session() as session:
        async with session.begin():
            db_category = await _category.get_by_id(session, category_id=category_id)
            if db_category is None:
                raise HTTPException(status_code=404, detail="Category not found")
            return db_category


@router.post("/{category_id}/items/", response_model=Item, status_code=201)
async def create_item_for_category(category_id: int,
                                   item: ItemCreate,
                                   shop_name: str = Body(...)):
    async with async_session() as session:
        async with session.begin():
            db_item = await _item.get_by_name(session, name=item.name)
            if db_item is not None:
                raise HTTPException(status_code=409, detail="Item already exists")
            db_shop = await _shop.get_by_name(session, name=shop_name)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return await _item.create(session,
                                      item=item,
                                      category_id=category_id,
                                      shop_id=db_shop.id)


@router.get("/{category_id}/items/", response_model=List[Item])
async def read_items_of_category(category_id: int):
    async with async_session() as session:
        async with session.begin():
            db_category = await _category.get_by_id(session, category_id=category_id)
            if db_category is None:
                raise HTTPException(status_code=404, detail="Category not found")
            return db_category.items
