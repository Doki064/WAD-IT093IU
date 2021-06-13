import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import models
import routers
from internal import admin
from database.config import engine

app = FastAPI(default_response_class=ORJSONResponse)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


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
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
