#!/usr/bin/env bash
# Manual fallback: inject server CPU spike via lab agent
set -euo pipefail
AGENT="${LAB_AGENT_URL:-http://127.0.0.1:9000}"
TOKEN="${LAB_AGENT_TOKEN:-change-me-agent}"
curl -sf -X POST "$AGENT/inject/server-spike" -H "x-agent-token: $TOKEN"
echo
