from routers.internal import APIRouter

from routers.endpoints import (
    customers,
    categories,
    items,
    shops,
    transactions,
    importations,
    details,
)
from routers import users

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(customers.router)
api_router.include_router(categories.router)
api_router.include_router(items.router)
api_router.include_router(shops.router)
api_router.include_router(transactions.router)
api_router.include_router(importations.router)
api_router.include_router(details.router)
