from typing import Optional

from pydantic import BaseModel as _BaseModel


# Schema for users
class UserBase(_BaseModel):
    username: str


class User(UserBase):
    uid: int
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


# Schema for tokens
class Token(_BaseModel):
    access_token: str
    token_type: str


class TokenData(_BaseModel):
    user_uid: Optional[int] = None
    username: Optional[str] = None
