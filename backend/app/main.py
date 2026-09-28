from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health, topology
from app.services.topology_service import TopologyService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.topology = TopologyService()
    yield


app = FastAPI(title="RootIQ API", version="0.1.0", lifespan=lifespan)
app.include_router(health.router, prefix="/api")
app.include_router(topology.router, prefix="/api")
