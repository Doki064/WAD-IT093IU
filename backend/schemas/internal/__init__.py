from typing import Optional
from uuid import UUID

import orjson
from sqlalchemy_utils import Password
from pydantic import BaseModel as _BaseModel


class BaseModelConfig(_BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


# Schema for users
class UserBase(BaseModelConfig):
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
class Token(BaseModelConfig):
    access_token: str
    token_type: str


class TokenPayload(_BaseModel):
    sub: Optional[UUID] = None
