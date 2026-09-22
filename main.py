from contextlib import asynccontextmanager
from database import create_tables
from fastapi import FastAPI
from router import router as workouts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app=FastAPI(lifespan=lifespan)

app.include_router(workouts_router)