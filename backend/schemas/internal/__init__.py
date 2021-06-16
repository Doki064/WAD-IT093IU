from typing import Optional
from uuid import UUID

from sqlalchemy_utils import Password
from pydantic import BaseModel as _BaseModel


# Schema for users
class UserBase(_BaseModel):
    username: str
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: Password
    salt: str

    class Config:
        arbitrary_types_allowed = True


class User(UserInDBBase):
    uuid: UUID


# Schema for tokens
class Token(_BaseModel):
    access_token: str
    token_type: str


class TokenPayload(_BaseModel):
    sub: Optional[UUID] = None
