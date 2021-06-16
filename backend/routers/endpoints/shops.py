"""All shop route methods."""
from typing import List, Union, Optional

from fastapi import HTTPException, Depends, Body

from routers.internal import APIRouter
from core.security import auth
from database.config import async_session
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
    prefix="/shops",
    tags=["shops"],
    dependencies=[Depends(auth.get_current_active_user)],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("", response_model=Shop)
async def create_shop(shop: ShopCreate, status_code=201):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_name(session, name=shop.name)
            if db_shop is not None:
                raise HTTPException(status_code=409, detail="Shop already exists")
            return await _shop.create(session, shop=shop)


@router.get("", response_model=Union[Shop, List[Shop]])
async def read_shops(
    shop_name: Optional[str] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None
):
    async with async_session() as session:
        async with session.begin():
            if shop_name is not None:
                db_shop = await _shop.get_by_name(session, name=shop_name)
                if db_shop is None:
                    raise HTTPException(status_code=404, detail="Shop not found")
                return db_shop
            return await _shop.get_all(session, skip=skip, limit=limit)


@router.get("/{shop_id}", response_model=Shop)
async def read_shop(shop_id: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_id(session, shop_id=shop_id)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop


@router.post("/{shop_id}/importations", response_model=Importation, status_code=201)
async def create_importation_for_shop(
    shop_id: int,
    importation: ImportationCreate,
    importation_details: List[ImportDetailCreate],
    item_name: str = Body(...)
):
    async with async_session() as session:
        async with session.begin():
            db_item = await _item.get_by_name(session, item_name)
            if db_item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            db_importation = await _importation.create(
                session, importation=importation, shop_id=shop_id
            )
            for detail in importation_details:
                await _import_detail.create(
                    session,
                    importation_detail=detail,
                    importation_id=db_importation.id,
                    item_id=db_item.id
                )

            return db_importation


@router.get("/{shop_id}/importations", response_model=List[Importation])
async def read_importations_of_shop(shop_id: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_id(session, shop_id=shop_id)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop.importations


@router.get("/{shop_id}/transactions", response_model=List[Transaction])
async def read_transactions_of_shop(shop_id: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_id(session, shop_id=shop_id)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop.transactions


@router.get("/{shop_id}/items", response_model=List[Item])
async def read_items_of_shop(shop_id: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_id(session, shop_id=shop_id)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop.items
