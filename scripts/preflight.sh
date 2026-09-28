#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
curl -fsS localhost:8000/api/health >/dev/null && echo "API ok" || echo "API down"
