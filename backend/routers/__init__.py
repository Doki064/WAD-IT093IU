from routers.internal import APIRouter

from routers import (
    users,
    customers,
    categories,
    items,
    shops,
    transactions,
    importations,
)

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(customers.router)
api_router.include_router(categories.router)
api_router.include_router(items.router)
api_router.include_router(shops.router)
api_router.include_router(transactions.router)
api_router.include_router(importations.router)
