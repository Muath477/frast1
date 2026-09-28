# RootIQ Contracts (frozen)

> Source of truth copied from Daily Plan §2.1–2.6. Any contract change = dedicated PR approved by every track.

## 2.1 Final topology (star around R1)

```text
                 ┌──────────────┐
                 │ R1 (vIOS)    │  Lo0 10.10.10.1 (management)
                 └─┬─────────┬──┘
     Gi0/0 10.10.20.1│         │Gi0/1 10.10.30.1
     (shaped 10 Mbps)│         │
          Gi0/1 ┌────┴──┐   ┌──┴────┐ Gi0/1
                │ SW1   │   │ SW2   │
                │.20.11 │   │.30.12 │
          Gi0/3 └───┬───┘   └───┬───┘ Gi0/3
                    │           │
             eth0 ┌─┴──────┐ ┌──┴──────────┐ ens3
                  │ APP-01 │ │ COLLECTOR-01│  + ens4 → EVE Cloud
                  │.20.10  │ │ .30.10      │
                  │DNS+Web │ │collector +  │
                  └────────┘ │lab-agent    │
                             └─────────────┘
Service path: COLLECTOR-01 → SW2 → R1(Gi0/1→Gi0/0) → SW1 → APP-01
```

| Device | Image | Address | Ports |
|---|---|---|---|
| R1 | Cisco vIOS (IOSv) | Lo0 `10.10.10.1/32` · Gi0/0 `10.10.20.1/24` · Gi0/1 `10.10.30.1/24` | Gi0/0→SW1 Gi0/1 · Gi0/1→SW2 Gi0/1 |
| SW1 | Cisco vIOS-L2 | Vlan1 `10.10.20.11/24` | Gi0/1→R1 · Gi0/3→APP-01 |
| SW2 | Cisco vIOS-L2 | Vlan1 `10.10.30.12/24` | Gi0/1→R1 · Gi0/3→COLLECTOR-01 |
| APP-01 | Ubuntu Server 24.04 | `10.10.20.10/24` gw `.1` | eth0→SW1 Gi0/3 |
| COLLECTOR-01 | Ubuntu Server 24.04 | ens3 `10.10.30.10/24` gw `.1` · ens4 DHCP (Cloud) | ens3→SW2 Gi0/3 |

Port names live **only** in `configs/topology.json` — never hardcode in app code.

## 2.2 Where everything runs

| Component | Where | Port |
|---|---|---|
| PostgreSQL 16 | Demo laptop (Docker) | 5432 |
| Backend FastAPI | Demo laptop (Docker) | 8000 |
| Frontend (dev) | Demo laptop | 5173 (proxy → 8000) |
| Frontend (build) | Demo laptop (nginx in Docker) | 8080 |
| Collector | COLLECTOR-01 in lab | → `http://<LAPTOP_IP>:8000/api/events/batch` |
| Lab-Agent | COLLECTOR-01 | 9000 |
| App-01 host agent | APP-01 | 9100 |

## 2.3 Stack (frozen)

- **Frontend:** Vite + React 19 + TypeScript + Tailwind CSS v4 + `@xyflow/react` + Zustand + React Router + Recharts + `motion` + `lucide-react` + `i18next` + Vitest + Playwright
- **Backend:** Python 3.12+ + FastAPI + Pydantic v2 + SQLAlchemy 2 + psycopg 3 + NetworkX + NumPy + scikit-learn + httpx + pytest
- **Lab:** EVE-NG + vIOS/vIOS-L2 + Ubuntu 24.04 + bind9 + nginx + iperf3 + stress-ng + net-snmp + Netmiko
- **Modes:** `ROOTIQ_MODE=live` | `ROOTIQ_MODE=sim` — UI only sees the badge

## 2.4 Normalized Event (single contract)

```json
{
  "eventId": "evt-00042",
  "timestamp": "2026-10-05T18:30:00Z",
  "sourceId": "link-r1-sw1",
  "sourceType": "link",
  "metric": "link_utilization",
  "value": 97.2,
  "unit": "percent",
  "interface": "Gi0/0",
  "severity": "info",
  "metadata": {"device": "r1", "peer": "sw1", "collector": "snmp"}
}
```

`sourceType ∈ router | switch | server | collector | link | service`

| metric | unit | on | warning | critical |
|---|---|---|---|---|
| `link_utilization` | percent | link | ≥ 70 | ≥ 85 |
| `link_latency_ms` | ms | link | ≥ 3× baseline or ≥ 30 | ≥ 60 |
| `link_packet_loss` | percent | link | ≥ 1 | ≥ 5 |
| `if_out_discards_rate` | pps | link | > 5 | > 50 |
| `if_oper_status` | 1/0 | link | — | = 0 |
| `cpu_percent` / `mem_percent` | percent | server | ≥ 80 / 85 | ≥ 95 |
| `http_latency_ms` | ms | service `svc-web` | ≥ 300 | ≥ 1000 |
| `http_ok` | 1/0 | service `svc-web` | — | = 0 |
| `dns_success_rate` | percent | service `svc-dns` | < 95 | < 50 |
| `dns_latency_ms` | ms | service `svc-dns` | ≥ 100 | ≥ 500 |

## 2.5 WebSocket messages (`/ws/operations`)

Envelope: `{type, ts, data}`

| type | data | frequency |
|---|---|---|
| `snapshot` | topology + status + open incidents + mode | once on connect |
| `link` | `{id,status,utilization,latencyMs,packetLoss}` | ≤ 1/s per link |
| `node` | `{id,status,metrics}` | ≤ 1/s |
| `service` | `{id,status,metrics}` | ≤ 1/s |
| `alert` | raw alert `{id,sourceId,metric,value,severity,ts}` | on threshold cross |
| `incident` | full incident object | on any change |
| `demo` | `{mode,scenario,state,injectedAt}` | inject/remediate/reset |

## 2.6 Incident lifecycle

`open → investigating → recommendation_ready → awaiting_approval → approved | rejected → resolved`

Reject does not change the lab; reason is logged. After reject, incident stays `awaiting_approval` for a new decision.
