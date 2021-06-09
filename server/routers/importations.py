"""All importation API methods."""
from typing import List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_database
from schemas import Importation, ImportDetail
from crud import importation as _importation
from crud import import_detail as _import_detail

router = APIRouter(
    prefix="/api/importations",
    tags=["importations"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/{importation_uid}", response_model=Importation)
def read_importation(importation_uid: int, db: Session = Depends(get_database)):
    db_importation = _importation.get_by_uid(db, importation_uid=importation_uid)
    if db_importation is None:
        raise HTTPException(status_code=404, detail="Importation not found")
    return db_importation


@router.get("/{date}", response_model=List[Importation])
def read_importations_by_date(date: datetime,
                              limit: int = 100,
                              db: Session = Depends(get_database)):
    db_importation = _importation.get_by_date(db, date=date, limit=limit)
    return db_importation


@router.get("/", response_model=List[Importation])
def read_importations(skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(get_database)):
    return _importation.get_all(db, skip=skip, limit=limit)


@router.get("/{importation_uid}/details/", response_model=List[ImportDetail])
def read_importation_details(importation_uid: int, db: Session = Depends(get_database)):
    db_importation_details = _import_detail.get_by_importation(
        db, importation_uid=importation_uid)
    return db_importation_details
