"""All user route methods."""
from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from routers.internal import APIRouter
from core.security import auth
from database.config import async_session
from schemas.internal import User, Token
from crud import user as _user
from core.config import settings

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/access-token", response_model=Token)
async def get_access_token(db_user: User):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth.create_access_token(uuid=db_user.uuid,
                                                  expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.authenticate(session, form_data.username,
                                               form_data.password)
            if db_user is None:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            elif db_user.is_active:
                raise HTTPException(status_code=400, detail="Inactive user")
            return RedirectResponse(url=f"{settings.API_PATH}/users/access-token")


@router.post("/register", status_code=201)
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_username(session, username=form_data.username)
            if db_user is not None:
                raise HTTPException(status_code=409, detail="Username already exists")
            await _user.create(session,
                               username=form_data.username,
                               password=form_data.password)
            return RedirectResponse(url=f"{settings.API_PATH}/users/access-token")


@router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user


@router.get("", response_model=User, dependencies=[Depends(auth.get_current_active_user)])
async def read_users(username: str):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_username(session, username=username)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user


@router.get("/{user_id}",
            response_model=User,
            dependencies=[Depends(auth.get_current_active_user)])
async def read_user(user_id: int):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_id(session, user_id=user_id)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user
