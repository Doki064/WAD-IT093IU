"""All importation route methods."""
from typing import List
from datetime import date

from fastapi import HTTPException, Depends    # noqa: F401

from routers.internal import APIRouter
# from core.security import auth
from database.config import async_session
from schemas import Importation, ImportDetail
from crud import importation as _importation
from crud.import_detail import get_importation_details

router = APIRouter(
    prefix="/importations",
    tags=["importations"],
    # dependencies=[Depends(auth.get_current_active_user)],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/min-max-dates")
async def read_min_max_dates():
    async with async_session() as session:
        async with session.begin():
            min_date = await _importation.get_min_date(session)
            max_date = await _importation.get_max_date(session)
            return {"min_date": min_date, "max_date": max_date}


@router.get("", response_model=List[Importation])
async def read_importations(skip: int = 0, limit: int = 1000):
    async with async_session() as session:
        async with session.begin():
            return await _importation.get_all(session, skip=skip, limit=limit)


@router.get("/date/{date}", response_model=List[Importation])
async def read_importations_by_date(date: date, limit: int = 1000):
    async with async_session() as session:
        async with session.begin():
            return await _importation.get_by_date(session, date=date, limit=limit)


@router.get("/{importation_id}", response_model=Importation)
async def read_importation(importation_id: int):
    async with async_session() as session:
        async with session.begin():
            db_importation = await _importation.get_by_id(
                session, importation_id=importation_id
            )
            if db_importation is None:
                raise HTTPException(status_code=404, detail="Importation not found")
            return db_importation


@router.get("/{importation_id}/details", response_model=List[ImportDetail])
async def read_importation_details(importation_id: int):
    async with async_session() as session:
        async with session.begin():
            db_importation_details = await get_importation_details(
                session, importation_id=importation_id
            )
            return db_importation_details
