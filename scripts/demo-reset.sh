#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
curl -fsS -X POST localhost:8000/api/demo/reset >/dev/null
echo "demo reset ok — waiting 20s for metrics to settle…"
sleep 20
exec ./scripts/preflight.sh
