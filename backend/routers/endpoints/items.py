"""All item route methods."""
from typing import List, Optional

from fastapi import HTTPException, Depends    # noqa: F401

from routers.internal import APIRouter
# from core.security import auth
from database.config import async_session
from schemas import Item
from crud import item as _item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(auth.get_current_active_user)],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("", response_model=List[Item])
async def read_items(item_name: Optional[str] = None, skip: int = 0, limit: int = 1000):
    async with async_session() as session:
        async with session.begin():
            if item_name is not None:
                return await _item.get_by_name(session, name=item_name)
            return await _item.get_all(session, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    async with async_session() as session:
        async with session.begin():
            db_item = await _item.get_by_id(session, item_id=item_id)
            if db_item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            return db_item
