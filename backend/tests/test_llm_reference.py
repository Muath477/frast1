"""Unit tests for the advisory LLM reference used when knowledge agents have a gap."""
from unittest.mock import AsyncMock, patch

import pytest

from app.llm import reference


@pytest.mark.asyncio
async def test_advise_returns_none_when_llm_disabled():
    with patch.object(reference.llm, "enabled", return_value=False):
        assert await reference.advise("knowledge", "no_kb_hit", {"conf": 80}) is None


@pytest.mark.asyncio
async def test_advise_rejects_ungrounded_numbers():
    with (
        patch.object(reference.llm, "enabled", return_value=True),
        patch.object(reference.llm, "complete", new=AsyncMock(return_value="Latency is 999 ms — reboot now.")),
    ):
        assert await reference.advise("knowledge", "no_kb_hit", {"conf": 80, "rootId": "L1"}) is None


@pytest.mark.asyncio
async def test_advise_accepts_grounded_text():
    with (
        patch.object(reference.llm, "enabled", return_value=True),
        patch.object(
            reference.llm,
            "complete",
            new=AsyncMock(return_value="Confidence is 80. Review metrics on L1 and compare with the playbook."),
        ),
    ):
        out = await reference.advise("knowledge", "no_kb_hit", {"conf": 80, "rootId": "L1"})
    assert out is not None
    assert out["source"] == "llm"
    assert out["gap"] == "no_kb_hit"
    assert out["agent"] == "knowledge"
    assert "80" in out["text"]
