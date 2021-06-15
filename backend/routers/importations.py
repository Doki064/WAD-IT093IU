"""All importation route methods."""
from typing import List, Optional
from datetime import date

from fastapi import HTTPException, Depends

from routers.internal import APIRouter
from security import auth
from database.config import async_session
from schemas import Importation, ImportDetail
from crud import importation as _importation

router = APIRouter(
    prefix="/importations",
    tags=["importations"],
    dependencies=[Depends(auth.get_current_active_user)],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/", response_model=List[Importation])
async def read_importations(skip: Optional[int] = None, limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            return await _importation.get_all(session, skip=skip, limit=limit)


@router.get("/date/{date}", response_model=List[Importation])
async def read_importations_by_date(date: date, limit: Optional[int] = None):
    async with async_session() as session:
        async with session.begin():
            return await _importation.get_by_date(session, date=date, limit=limit)


@router.get("/{importation_id}", response_model=Importation)
async def read_importation(importation_id: int):
    async with async_session() as session:
        async with session.begin():
            db_importation = await _importation.get_by_id(session,
                                                          importation_id=importation_id)
            if db_importation is None:
                raise HTTPException(status_code=404, detail="Importation not found")
            return db_importation


@router.get("/{importation_id}/details/", response_model=List[ImportDetail])
async def read_importation_details(importation_id: int):
    async with async_session() as session:
        async with session.begin():
            db_importation = await _importation.get_by_id(session,
                                                          importation_id=importation_id)
            return db_importation.importation_details
