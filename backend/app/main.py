from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health, topology


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Day 3+: load topology, create tables, start simulator
    yield


app = FastAPI(title="RootIQ API", version="0.1.0", lifespan=lifespan)
app.include_router(health.router, prefix="/api")
app.include_router(topology.router, prefix="/api")
