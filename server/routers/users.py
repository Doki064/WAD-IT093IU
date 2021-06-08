from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import encryption
import database
import crud.user as crud
from schemas import User, UserCreate


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{username}", response_model=User)
def check_user(username: str, password: str):
    db: Session = Depends(database.get_db())
    db_user = crud.get_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        if not encryption.check_password(db_user.hashed_password, password):
            return None
    except encryption.NeedRehashException:
        crud.update_password(db, user_uid=db_user.uid, password=password)
    return db_user


@router.post("/", response_model=User)
def create_user(user: UserCreate):
    db: Session = Depends(database.get_db())
    db_user = crud.get_by_username(db, username=user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create(db, user=user)


@router.get("/{user_uid}", response_model=User)
def read_user(user_uid: int):
    db: Session = Depends(database.get_db)
    db_user = crud.get_user(db, user_id=user_uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
