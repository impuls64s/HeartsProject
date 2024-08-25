import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import auth, profile
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Initializing DB...')
    await init_db()
    yield
    print('Shutting down...')


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(profile.router, prefix="", tags=["Profile"])

