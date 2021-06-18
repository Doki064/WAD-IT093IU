"""All internal API methods for admin only."""
from typing import Dict, List
from datetime import date

import pandas as pd
import plotly.express as px
from aioify import aioify
from fastapi import HTTPException, Query
from fastapi.responses import PlainTextResponse

import models
from schemas import TransactionPlot, TransactDetail
from routers.internal import APIRouter
from database.config import async_session
from crud import transaction as _transaction

router = APIRouter(
    prefix="/internal/admin",
    tags=["admin"],
    responses={418: {
        "description": "I'm a teapot"
    }},
)


@router.get("")
def read_table_info() -> Dict[str, List[str]]:
    response = dict()
    for model in models.__all__:
        key = getattr(models, model).__tablename__
        value = getattr(models, model).__table__.c.keys()
        response[key] = value
    return response


@router.get("/plot")
async def read_transaction_plot(
    start_date: date,
    end_date: date,
    shop_ids: List[int] = Query(None),
    skip: int = 0,
    limit: int = 1000000
):
    async with async_session() as session:
        async with session.begin():
            db_transactions = await _transaction.get_all_with_details(
                session, skip=skip, limit=limit
            )
            db_details = [
                db_detail for db_transaction in db_transactions
                for db_detail in db_transaction.transaction_details
            ]
            transactions = [
                dict(TransactionPlot.from_orm(transaction))
                for transaction in db_transactions
            ]
            details = [dict(TransactDetail.from_orm(detail)) for detail in db_details]
            transactions_df = pd.DataFrame.from_records(transactions)
            details_df = pd.DataFrame.from_records(details)
            df = pd.merge(
                transactions_df, details_df, left_on="id", right_on="transaction_id"
            )
            df = df.drop(["id", "status", "transaction_id"], axis=1)
            fig = await plot(df, start_date, end_date, shop_ids)
            return PlainTextResponse(fig.to_json(), media_type="application/json")


@router.get("/table")
async def read_table_statistics():
    raise HTTPException(status_code=501)


async def plot(df, start_date: date, end_date: date, shop_ids):
    days_in_between = end_date - start_date
    selected_df = await _select_df_in_between(
        df,
        start_date,
        end_date,
        shop_ids,
    )
    if days_in_between.days <= 90:
        profit_df = await _group_by(selected_df, "W-MON")

    else:
        profit_df = await _group_by(selected_df, "M")

    plot_title = f" profit of shop {shop_ids} from {start_date} to {end_date}"

    if profit_df.empty:
        fig = px.line(title="A beautiful blank chart", template="plotly")
    if days_in_between.days <= 90:
        fig = px.line(
            profit_df,
            x="date",
            y="profit",
            title="Weekly" + plot_title,
            template="plotly"
        )    # Plotly line chart
    else:
        fig = px.line(
            profit_df,
            x="date",
            y="profit",
            title="Monthly" + plot_title,
            template="plotly",
            color="shop_id"
        )    # Plotly
    fig.update_layout(title_x=0.5)
    return fig


@aioify
def _select_df_in_between(df, start_date, end_date, shop_ids):
    """Get subset of DF that is between given dates

    Arguments:
         df: pandas DataFrame.
         start_date (datetime): The start date to select
         end_date (datetime): The end date to select. `start_date` <= `end_date`
         shop_ids (int): The shop id to select
    Returns:
        selected_df: pandas DataFrame. Subset of the DF with the given condition
    """

    selected_df = df[(df["date"].between(start_date, end_date)) &
                     (df["shop_id"].isin(shop_ids))]
    # selected_df["profit"] = selected_df["itemPrice"] * selected_df["transactionAmount"]
    selected_df.loc[:, "profit"] = selected_df.loc[:, "item_price"].multiply(
        selected_df.loc[:, "item_amount"], axis="index"
    )
    return selected_df


@aioify
def _group_by(df, freq):
    """Group DF by freq

    Arguments:
        df: pandas DataFrame. The DF that needs to group by column "date"
        freq: string. Either "W-MON" (weekly group) or "M" (monthly group)

    Returns:
         profit_df: pandas DataFrame. The grouped DF by freq, with profit calculated.
    """
    df["date"] = pd.to_datetime(df["date"]) - pd.to_timedelta(7, unit="d")
    profit_df = df.groupby([pd.Grouper(key="date", freq=freq), "shop_id"])["profit"] \
        .sum() \
        .reset_index() \
        .sort_values("date")  # Group by week
    return profit_df
