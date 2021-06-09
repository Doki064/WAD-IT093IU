import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from database import config
import routers

config.create_database()

app = FastAPI(debug=True)
app.include_router(routers.users_router)
app.include_router(routers.customers_router)
app.include_router(routers.categories_router)
app.include_router(routers.items_router)
app.include_router(routers.shops_router)
app.include_router(routers.transactions_router)
app.include_router(routers.importations_router)


@app.get("/")
def root():
    return RedirectResponse(url="/docs/")


@app.get("/api/")
def main():
    return {"message": "Hello, Docker!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
