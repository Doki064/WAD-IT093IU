"""All item API methods."""
from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException

from database.config import async_session
from schemas import Item
from crud import item as _item

router = APIRouter(
    prefix="/api/items",
    tags=["items"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/", response_model=Union[Item, List[Item]])
async def read_items(item_name: Optional[str] = None, skip: int = 0, limit: int = 100):
    async with async_session() as session:
        async with session.begin():
            if item_name is not None:
                db_item = await _item.get_by_name(session, name=item_name)
                if db_item is None:
                    raise HTTPException(status_code=404, detail="Item not found")
                return db_item
            return await _item.get_all(session, skip=skip, limit=limit)


@router.get("/{item_uid}", response_model=Item)
async def read_item(item_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_item = await _item.get_by_uid(session, item_uid=item_uid)
            if db_item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            return db_item
