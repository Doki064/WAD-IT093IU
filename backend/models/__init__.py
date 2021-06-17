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

from uuid import uuid4

from sqlalchemy import (
    Column,
    ForeignKey,
    CheckConstraint,
    Boolean,
    Integer,
    Float,
    String,
    Date,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import functions
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType, force_auto_coercion

from database.config import Base
from core.config import settings

force_auto_coercion()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(
        PasswordType(
            onload=lambda **kwargs: dict(
                schemes=settings.SCHEMES,
                deprecated="auto",
                **kwargs,
            )
        ),
        nullable=False
    )
    salt = Column(String(32), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    __mapper_args__ = {"eager_defaults": True}


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)

    transactions = relationship("Transaction", back_populates="customer", lazy="raise")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    quantity = Column(Integer, CheckConstraint("quantity >= 0"), default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))

    category = relationship("Category", back_populates="items")
    shop = relationship("Shop", back_populates="items")

    __mapper_args__ = {"eager_defaults": True}


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)

    importations = relationship("Importation", back_populates="shop", lazy="raise")
    transactions = relationship("Transaction", back_populates="shop", lazy="raise")
    items = relationship("Item", back_populates="shop")


class Importation(Base):
    __tablename__ = "importations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(
        Date, index=True, nullable=False, server_default=functions.current_date()
    )
    shop_id = Column(Integer, ForeignKey("shops.id"))

    importation_details = relationship(
        "ImportDetail", back_populates="importation", lazy="immediate"
    )
    shop = relationship("Shop", back_populates="importations")

    __mapper_args__ = {"eager_defaults": True}


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(
        Date, index=True, nullable=False, server_default=functions.current_date()
    )
    status = Column(String(20), default="PENDING")
    customer_id = Column(Integer, ForeignKey("customers.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))

    transaction_details = relationship(
        "TransactDetail", back_populates="transaction", lazy="immediate"
    )
    customer = relationship("Customer", back_populates="transactions")
    shop = relationship("Shop", back_populates="transactions")

    __mapper_args__ = {"eager_defaults": True}


class ImportDetail(Base):
    __tablename__ = "importation_details"

    importation_id = Column(Integer, ForeignKey("importations.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    item_amount = Column(Integer, CheckConstraint("item_amount > 0"))

    importation = relationship("Importation", back_populates="importation_details")
    item = relationship("Item", foreign_keys=item_id)


class TransactDetail(Base):
    __tablename__ = "transaction_details"

    transaction_id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    item_price = Column(Float, nullable=False)
    item_amount = Column(Integer, CheckConstraint("item_amount > 0"))

    transaction = relationship("Transaction", back_populates="transaction_details")
    item = relationship("Item", foreign_keys=item_id)
