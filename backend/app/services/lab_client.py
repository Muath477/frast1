import httpx

from app.core.config import settings


async def call(path: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post(
            f"{settings.lab_agent_url}{path}",
            headers={"x-agent-token": settings.lab_agent_token},
        )
        r.raise_for_status()
        return r.json()
