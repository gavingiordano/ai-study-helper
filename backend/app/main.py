from contextlib import asynccontextmanager

from app import routes
from app.database import create_db_and_tables
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}