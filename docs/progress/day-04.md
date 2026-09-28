# Day 04 — Live collector + NOC shell

## Acceptance
- [x] `lab/collector/collector.py` + systemd unit (SNMP / hop-diff ICMP / DNS+HTTP / agent)
- [x] `lab/app01/agent.py` + `rootiq-agent.service` (`:9100/metrics`)
- [x] `poll_timeout` in thresholds (crit at ≥0.5)
- [x] TopBar: RootIQ · LIVE LAB / SIMULATION · WS · Last update · lang placeholder
- [x] KPI Strip — 6 cards
- [x] `DevicesPage` — searchable table (5 nodes)
- [x] Services panel on map · DeviceInspector live CPU/Mem bars
- [x] `detector.py` + `test_detector.py` — **3 passed**
- [ ] Live EVE: collector push / iperf util / journalctl — INFRA deferred
- [x] Tag `day-04`
