__all__ = [
    "User",
    "UserCreate",
    "Customer",
    "CustomerCreate",
    "Category",
    "CategoryCreate",
    "Item",
    "ItemCreate",
    "Shop",
    "ShopCreate",
    "Importation",
    "ImportationCreate",
    "Transaction",
    "TransactionCreate",
    "ImportDetail",
    "ImportDetailCreate",
    "TransactDetail",
    "TransactDetailCreate",
]

from typing import List

from pydantic import BaseModel as _BaseModel


# Schema for importation details
class ImportDetailBase(_BaseModel):
    item_amount: int


class ImportDetailCreate(ImportDetailBase):
    pass


class ImportDetail(ImportDetailBase):
    importation_uid: int
    item_uid: int

    class Config:
        orm_mode = True


# Schema for importations
class ImportationBase(_BaseModel):
    date: str


class ImportationCreate(ImportationBase):
    pass


class Importation(ImportationBase):
    uid: int
    shop_uid: int
    importation_details: List[ImportDetail] = []

    class Config:
        orm_mode = True


# Schema for transaction details
class TransactDetailBase(_BaseModel):
    item_price: float
    item_amount: int


class TransactDetailCreate(TransactDetailBase):
    pass


class TransactDetail(TransactDetailBase):
    transaction_uid: int
    item_uid: int

    class Config:
        orm_mode = True


# Schema for transactions
class TransactionBase(_BaseModel):
    date: str
    status: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    uid: int
    customer_uid: int
    shop_uid: int
    transaction_details: List[TransactDetail] = []

    class Config:
        orm_mode = True


# Schema for items
class ItemBase(_BaseModel):
    name: str
    quantity: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    uid: int
    category_uid: int
    shop_uid: int

    class Config:
        orm_mode = True


# Schema for categories
class CategoryBase(_BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    uid: int
    items: List[Item] = []

    class Config:
        orm_mode = True


# Schema for shops
class ShopBase(_BaseModel):
    name: str


class ShopCreate(ShopBase):
    pass


class Shop(ShopBase):
    uid: int
    importations: List[Importation] = []
    transactions: List[Transaction] = []
    items: List[Item] = []

    class Config:
        orm_mode = True


# Schema for customers
class CustomerBase(_BaseModel):
    name: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    uid: int
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True


# Schema for users
class UserBase(_BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uid: int

    class Config:
        orm_mode = True
