__all__ = [
    "User",
    "Customer",
    "Category",
    "Item",
    "Shop",
    "Importation",
    "Transaction",
    "ImportDetail",
    "TransactDetail",
]

from sqlalchemy import (
    Column,
    ForeignKey,
    CheckConstraint,
    Integer,
    Float,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship


from database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = "customers"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    transactions = relationship("Transaction", back_populates="customer")


class Category(Base):
    __tablename__ = "categories"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    items = relationship("Category", back_populates="category")


class Item(Base):
    __tablename__ = "items"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Integer, CheckConstraint("quantity >= 0"), default=0)
    category_uid = Column(Integer, ForeignKey("categories.uid"))
    shop_uid = Column(Integer, ForeignKey("shops.uid"))

    category = relationship("Category", back_populates="items")
    shop = relationship("Shop", back_populates="items")


class Shop(Base):
    __tablename__ = "shops"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    importations = relationship("Importation", back_populates="shop")
    transactions = relationship("Transaction", back_populates="shop")
    items = relationship("Item", back_populates="shop")


class Importation(Base):
    __tablename__ = "importations"

    uid = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    shop_uid = Column(Integer, ForeignKey("shops.uid"))

    importation_details = relationship("ImportDetail", back_populates="importation")
    shop = relationship("Shop", back_populates="importations")


class Transaction(Base):
    __tablename__ = "transactions"

    uid = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    status = Column(String, default="PENDING")
    customer_uid = Column(Integer, ForeignKey("customers.uid"))
    shop_uid = Column(Integer, ForeignKey("shops.uid"))

    transaction_details = relationship("TransactDetail", back_populates="transaction")
    customer = relationship("Customer", back_populates="transactions")
    shop = relationship("Shop", back_populates="transactions")


class ImportDetail(Base):
    __tablename__ = "importation_details"

    importation_uid = Column(Integer, ForeignKey("importations.uid"), primary_key=True)
    item_uid = Column(Integer, ForeignKey("items.uid"), primary_key=True)
    item_amount = Column(Integer, CheckConstraint("item_amount > 0"))

    importation = relationship("Importation", back_populates="importation_details")
    item = relationship("Item")


class TransactDetail(Base):
    __tablename__ = "transaction_details"

    transaction_uid = Column(Integer, ForeignKey("transactions.uid"), primary_key=True)
    item_uid = Column(Integer, ForeignKey("items.uid"), primary_key=True)
    item_price = Column(Float, nullable=False)
    item_amount = Column(Integer, CheckConstraint("item_amount > 0"))

    transaction = relationship("Transaction", back_populates="transaction_details")
    item = relationship("Item")