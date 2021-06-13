"""All shop route methods."""
from typing import List, Union, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Body

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
    prefix="/api/shops",
    tags=["shops"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/", response_model=Shop)
async def create_shop(shop: ShopCreate):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_name(session, name=shop.name)
            if db_shop is not None:
                raise HTTPException(status_code=400, detail="Shop already exists")
            return await _shop.create(session, shop=shop)


@router.get("/", response_model=Union[Shop, List[Shop]])
async def read_shops(shop_name: Optional[str] = None,
                     skip: Optional[int] = None,
                     limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            if shop_name is not None:
                db_shop = await _shop.get_by_name(session, name=shop_name)
                if db_shop is None:
                    raise HTTPException(status_code=404, detail="Shop not found")
                return db_shop
            return await _shop.get_all(session, skip=skip, limit=limit)


@router.get("/{shop_uid}", response_model=Shop)
async def read_shop(shop_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_uid(session, shop_uid=shop_uid)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop


@router.post("/{shop_uid}/importations/", response_model=Importation)
async def create_importation_for_shop(shop_uid: int,
                                      importation: ImportationCreate,
                                      background_tasks: BackgroundTasks,
                                      importation_details: List[ImportDetailCreate],
                                      item_name: str = Body(...)):
    async with async_session() as session:
        async with session.begin():
            db_item = await _item.get_by_name(session, item_name)
            if db_item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            db_importation = await _importation.create(session,
                                                       importation=importation,
                                                       shop_uid=shop_uid)
            # for detail in importation_details:
            #     await _import_detail.create(session,
            #                                 importation_detail=detail,
            #                                 importation_uid=db_importation.uid,
            #                                 item_uid=db_item.uid)
            background_tasks.add_task(_create_importation_details, session,
                                      importation_details, db_importation.uid,
                                      db_item.uid)
            return db_importation


@router.get("/{shop_uid}/importations/", response_model=List[Importation])
async def read_importations_of_shop(shop_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_uid(session, shop_uid=shop_uid)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop.importations


@router.get("/{shop_uid}/transactions/", response_model=List[Transaction])
async def read_transactions_of_shop(shop_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_uid(session, shop_uid=shop_uid)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop.transactions


@router.get("/{shop_uid}/items/", response_model=List[Item])
async def read_items_of_shop(shop_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_shop = await _shop.get_by_uid(session, shop_uid=shop_uid)
            if db_shop is None:
                raise HTTPException(status_code=404, detail="Shop not found")
            return db_shop.items


async def _create_importation_details(session,
                                      importation_details: List[ImportDetailCreate],
                                      importation_uid: int, item_uid: int):
    for detail in importation_details:
        await _import_detail.create(session,
                                    importation_details=detail,
                                    importation_uid=importation_uid,
                                    item_uid=item_uid)
