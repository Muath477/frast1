#!/usr/bin/env bash
set -uo pipefail
ok(){ printf "  \033[32m✔\033[0m %s\n" "$1"; }; bad(){ printf "  \033[31m✘\033[0m %s\n" "$1"; FAIL=1; }
FAIL=0; COLLECTOR=${COLLECTOR:-192.168.100.50}
echo "RootIQ preflight"
curl -sf localhost:8000/api/health >/dev/null && ok "backend" || bad "backend"
curl -sf localhost:8080 >/dev/null && ok "frontend (8080)" || bad "frontend (optional if using Vite :5173)"
docker compose ps db 2>/dev/null | grep -q healthy && ok "postgres" || bad "postgres (optional on laptop)"
curl -sf -m 3 "http://$COLLECTOR:9000/health" >/dev/null && ok "lab-agent" || bad "lab-agent (use sim)"
MODE=$(curl -s localhost:8000/api/health | python3 -c "import sys,json;print(json.load(sys.stdin).get('mode','?'))" 2>/dev/null || echo "?")
ok "mode = $MODE"
N=$(curl -s localhost:8000/api/incidents | python3 -c "import sys,json;print(len([i for i in json.load(sys.stdin) if i.get('status')!='resolved']))" 2>/dev/null || echo "?")
[ "$N" = "0" ] && ok "no open incidents" || bad "$N open incidents → run scripts/demo-reset.sh"
[ -f docs/demo-backup.mp4 ] && ok "backup video present" || bad "backup video missing (deferred)"
exit $FAIL
