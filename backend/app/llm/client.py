"""Provider-neutral LLM client (Anthropic / Gemini / Groq).

Every caller in RootIQ treats the LLM as an optional *wording* layer:
`complete()` never raises and returns None when the LLM is disabled, missing a key,
slow, or broken — the caller then falls back to its deterministic answer.
"""
from __future__ import annotations

import time

import httpx

from app.core.config import settings

DEFAULT_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",
    "gemini": "gemini-2.5-flash",
    "groq": "llama-3.3-70b-versatile",
}
PROVIDERS = tuple(DEFAULT_MODELS)


def _key(provider: str) -> str:
    return {
        "anthropic": settings.anthropic_api_key,
        "gemini": settings.gemini_api_key,
        "groq": settings.groq_api_key,
    }.get(provider, "")


def model_name(provider: str | None = None) -> str:
    provider = provider or settings.llm_provider
    return settings.llm_model or DEFAULT_MODELS.get(provider, "")


def enabled() -> bool:
    return bool(
        settings.llm_enabled
        and settings.llm_provider in PROVIDERS
        and _key(settings.llm_provider)
    )


# Usage counters (per process) so operators can watch cost and reliability.
# Character counts are a cheap proxy for tokens (about 4 characters per token).
USAGE = {"calls": 0, "errors": 0, "totalMs": 0.0, "charsIn": 0, "charsOut": 0}


def usage() -> dict:
    calls = USAGE["calls"]
    return {
        **USAGE,
        "avgMs": round(USAGE["totalMs"] / calls, 1) if calls else 0.0,
        "approxTokensIn": USAGE["charsIn"] // 4,
        "approxTokensOut": USAGE["charsOut"] // 4,
    }


def info() -> dict:
    """Safe-to-expose LLM status (never includes keys)."""
    return {
        "enabled": enabled(),
        "provider": settings.llm_provider,
        "model": model_name(),
        "requested": bool(settings.llm_enabled),
        "usage": usage(),
    }


async def _post(url: str, headers: dict, payload: dict, timeout: float) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as c:
        r = await c.post(url, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()


async def _anthropic(system: str, user: str, max_tokens: int, timeout: float) -> str:
    data = await _post(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": settings.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        {
            "model": model_name("anthropic"),
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        },
        timeout,
    )
    return "".join(b.get("text", "") for b in data["content"])


async def _gemini(system: str, user: str, max_tokens: int, timeout: float) -> str:
    data = await _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name('gemini')}:generateContent",
        {"x-goog-api-key": settings.gemini_api_key, "content-type": "application/json"},
        {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.1},
        },
        timeout,
    )
    parts = data["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts)


async def _groq(system: str, user: str, max_tokens: int, timeout: float) -> str:
    data = await _post(
        "https://api.groq.com/openai/v1/chat/completions",
        {
            "authorization": f"Bearer {settings.groq_api_key}",
            "content-type": "application/json",
        },
        {
            "model": model_name("groq"),
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout,
    )
    return data["choices"][0]["message"]["content"]


_IMPL = {"anthropic": _anthropic, "gemini": _gemini, "groq": _groq}


async def complete(
    system: str, user: str, max_tokens: int = 300, timeout: float = 6.0
) -> str | None:
    if not enabled():
        return None
    t0 = time.perf_counter()
    USAGE["calls"] += 1
    USAGE["charsIn"] += len(system) + len(user)
    try:
        text = await _IMPL[settings.llm_provider](system, user, max_tokens, timeout)
    except Exception:
        USAGE["errors"] += 1
        return None
    finally:
        USAGE["totalMs"] += (time.perf_counter() - t0) * 1000
    text = (text or "").strip()
    USAGE["charsOut"] += len(text)
    return text or None
