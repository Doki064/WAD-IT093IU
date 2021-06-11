import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from database.config import engine, Base
import routers

app = FastAPI()


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def root():
    return RedirectResponse(url="/docs/")


@app.get("/api/")
def main():
    return {"message": "Hello, Docker!"}


app.include_router(routers.users_router)
app.include_router(routers.customers_router)
app.include_router(routers.categories_router)
app.include_router(routers.items_router)
app.include_router(routers.shops_router)
app.include_router(routers.transactions_router)
app.include_router(routers.importations_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
