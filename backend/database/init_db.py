# import csv
from pathlib import Path
# from datetime import date

import asyncpg
import pandas as pd
from sqlalchemy import exc

from database.config import async_session
from schemas.internal import UserCreate
# from schemas import (
#     CustomerCreate,
#     CategoryCreate,
#     ShopCreate,
#     ItemCreate,
#     ImportationCreate,
#     ImportDetailCreate,
#     TransactionCreate,
#     TransactDetailCreate,
# )
from crud import user
from core.config import settings


async def init_user():
    async with async_session() as session:
        async with session.begin():
            superuser = UserCreate(
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_active=True,
                is_superuser=True
            )
            try:
                await user.create(session, user=superuser)
            except exc.IntegrityError:
                pass


async def init_data():
    data_dir = Path(__file__).parent.joinpath("dummy_data").resolve()
    con = await asyncpg.connect(
        host=settings.POSTGRES_HOST,
        port="5432",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB
    )
    files = [
        "customers",
        "categories",
        "shops",
        "items",
        "importations",
        "transactions",
        "importation_details",
        "transaction_details",
    ]
    for file in files:
        f = data_dir.joinpath(f"{file}.csv")
        df = pd.read_csv(f)
        try:
            df["date"] = pd.to_datetime(df["date"])
        except Exception:
            pass
        records = [tuple(x) for x in df.values]
        print(f"Importing {file} ....")
        try:
            await con.copy_records_to_table(
                f.stem, records=records, columns=list(df.columns)
            )
        except asyncpg.exceptions.UniqueViolationError:
            break


# async def init_data():
#     data_dir = Path(__file__).parent.joinpath("dummy_data").resolve()
#     with open(f"{data_dir}/customers.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if count == 0 or int(row["id"]) == 0:
#                 continue
#             record = CustomerCreate(name=row["name"])
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await customer.create(session, customer=record)
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/categories.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if count == 0 or int(row["id"]) == 0:
#                 continue
#             record = CategoryCreate(name=row["name"])
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await category.create(session, category=record)
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/shops.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if count == 0 or int(row["id"]) == 0:
#                 continue
#             record = ShopCreate(name=row["name"])
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await shop.create(session, shop=record)
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/items.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if (
#                 count == 0 or int(row["id"]) == 0 or int(row["category_id"]) == 0
#                 or int(row["shop_id"]) == 0
#             ):
#                 continue
#             record = ItemCreate(name=row["name"], quantity=int(row["quantity"]))
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await item.create(
#                             session,
#                             item=record,
#                             category_id=int(row["category_id"]),
#                             shop_id=int(row["shop_id"])
#                         )
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/importations.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if count == 0 or int(row["id"]) == 0 or int(row["shop_id"]) == 0:
#                 continue
#             record = ImportationCreate(date=date.fromisoformat(row["date"]))
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await importation.create(
#                             session, importation=record, shop_id=int(row["shop_id"])
#                         )
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/importation_details.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if count == 0 or int(row["importation_id"]) == 0 or int(row["item_id"]) == 0:
#                 continue
#             record = ImportDetailCreate(item_amount=int(row["item_amount"]))
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await import_detail.create(
#                             session,
#                             importation_detail=record,
#                             importation_id=int(row["importation_id"]),
#                             item_id=int(row["item_id"])
#                         )
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/transactions.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if (
#                 count == 0 or int(row["id"]) == 0 or int(row["customer_id"]) == 0
#                 or int(row["shop_id"]) == 0
#             ):
#                 continue
#             record = TransactionCreate(
#                 date=date.fromisoformat(row["date"]), status=row["status"]
#             )
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await transaction.create(
#                             session,
#                             transaction=record,
#                             customer_id=int(row["customer_id"]),
#                             shop_id=int(row["shop_id"])
#                         )
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break

#     with open(f"{data_dir}/transaction_details.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for count, row in enumerate(csv_reader):
#             if count == 0 or int(row["transaction_id"]) == 0 or int(row["item_id"]) == 0:
#                 continue
#             record = TransactDetailCreate(
#                 item_price=float(row["item_price"]), item_amount=int(row["item_amount"])
#             )
#             async with async_session() as session:
#                 async with session.begin():
#                     try:
#                         await transact_detail.create(
#                             session,
#                             transaction_detail=record,
#                             transaction_id=int(row["transaction_id"]),
#                             item_id=int(row["item_id"])
#                         )
#                     except exc.IntegrityError:
#                         if count == 1:
#                             break


async def init():
    await init_user()
    await init_data()
