from typing import List

from routers.internal import APIRouter
# from core.security import auth
from database.config import async_session
from schemas import TransactDetail, ImportDetail
from crud.transact_detail import get_all as get_transaction_details
from crud.import_detail import get_all as get_importation_details

router = APIRouter()


@router.get(
    "/transaction_details", tags=["transactions"], response_model=List[TransactDetail]
)
async def read_transaction_details(skip: int = 0, limit: int = 1000):
    async with async_session() as session:
        async with session.begin():
            return await get_transaction_details(session, skip=skip, limit=limit)


@router.get(
    "/importation_details", tags=["importations"], response_model=List[ImportDetail]
)
async def read_importation_details(skip: int = 0, limit: int = 1000):
    async with async_session() as session:
        async with session.begin():
            return await get_importation_details(session, skip=skip, limit=limit)
