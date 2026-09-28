"""Replay recorded events into POST /api/events/batch (demo fallback)."""
from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path

import httpx


async def replay(path: Path, backend: str, token: str, speed: float) -> None:
    lines = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        raise SystemExit(f"empty recording: {path}")
    t0 = float(lines[0]["ts"])
    wall0 = time.monotonic()
    async with httpx.AsyncClient(timeout=10.0) as client:
        batch: list[dict] = []
        last_flush = wall0
        for row in lines:
            target = wall0 + (float(row["ts"]) - t0) / max(speed, 0.01)
            delay = target - time.monotonic()
            if delay > 0:
                await asyncio.sleep(delay)
            batch.append(
                {
                    "sourceId": row["sourceId"],
                    "sourceType": row.get("sourceType", "link"),
                    "metric": row["metric"],
                    "value": row["value"],
                    "unit": row.get("unit", ""),
                    "interface": row.get("interface"),
                    "timestamp": row.get("timestamp"),
                    "metadata": {"collector": "replay", "file": path.name},
                }
            )
            if len(batch) >= 20 or time.monotonic() - last_flush > 1.0:
                await client.post(
                    f"{backend.rstrip('/')}/api/events/batch",
                    json={"events": batch},
                    headers={"x-rootiq-token": token},
                )
                batch, last_flush = [], time.monotonic()
        if batch:
            await client.post(
                f"{backend.rstrip('/')}/api/events/batch",
                json={"events": batch},
                headers={"x-rootiq-token": token},
            )
    print(f"replayed {len(lines)} events from {path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Replay RootIQ event recordings")
    p.add_argument("file", type=Path)
    p.add_argument("--backend", default="http://127.0.0.1:8000")
    p.add_argument("--token", default="change-me-ingest")
    p.add_argument("--speed", type=float, default=1.0)
    args = p.parse_args()
    asyncio.run(replay(args.file, args.backend, args.token, args.speed))


if __name__ == "__main__":
    main()
