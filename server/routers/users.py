"""All user API methods."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import encryption
from database import get_database
import crud.user as crud
from schemas import User, UserCreate

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/login/", response_model=User)
def check_user(user: UserCreate, db: Session = Depends(get_database)):
    db_user = crud.get_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        salt = bytes.fromhex(db_user.salt)
        if not encryption.check_password(db_user.hashed_password, user.password, salt):
            return None
    except encryption.NeedRehashException:
        crud.update_password(db, user_uid=db_user.uid, password=user.password)
    return db_user


@router.post("/register/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_database)):
    db_user = crud.get_by_username(db, username=user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create(db, user=user)


@router.get("/{user_uid}", response_model=User)
def read_user_by_uid(user_uid: int, db: Session = Depends(get_database)):
    db_user = crud.get_by_uid()(db, user_uid=user_uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{username}", response_model=User)
def read_user_by_username(username: str, db: Session = Depends(get_database)):
    db_user = crud.get_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return crud.get_all(db, skip=skip, limit=limit)
