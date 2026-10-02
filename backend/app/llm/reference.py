"""Advisory LLM reference when a knowledge-layer agent has an empty KB hit.

Used by Knowledge / Vendor only. Never invents RCA numbers, never produces
executable commands — callers treat the result as engineer-facing advice.
Returns None quietly when the LLM is off, fails, or fails the grounding check.
"""
from __future__ import annotations

import json

from app.intelligence.explain import grounded
from app.llm import client as llm

SYSTEM = (
    "You are a NOC advisory reference for RootIQ. Another agent had no curated answer. "
    "Use ONLY the facts JSON. Never invent a number that is not in the facts. "
    "Never invent CLI commands or change procedures that look executable. "
    "Reply with a few short advisory sentences for the engineer. Western digits only. "
    "If facts are insufficient, say what to check next without guessing values."
)


async def advise(
    agent_id: str,
    gap: str,
    facts: dict,
    *,
    lang: str = "en",
) -> dict | None:
    """Ask the LLM for advisory text when a knowledge agent has a gap.

    Returns ``{text, source, gap, agent}`` or ``None``.
    """
    if not llm.enabled():
        return None
    prompt = (
        f"AGENT: {agent_id}\n"
        f"GAP: {gap}\n"
        f"LANG: {'Arabic' if lang == 'ar' else 'English'}\n"
        f"FACTS: {json.dumps(facts, ensure_ascii=False)}"
    )
    text = await llm.complete(SYSTEM, prompt, max_tokens=180, timeout=5.0)
    if not text or not grounded(text, facts):
        return None
    return {
        "text": text.strip(),
        "source": "llm",
        "gap": gap,
        "agent": agent_id,
    }
