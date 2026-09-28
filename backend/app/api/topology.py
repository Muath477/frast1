import json
from pathlib import Path

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["topology"])


@router.get("/topology")
def get_topology():
    return json.loads(Path(settings.topology_path).read_text(encoding="utf-8"))
