# Day 02 — Real topology (ports + custom edges)

## Acceptance
- [x] `DeviceNode` + `PortEdge` + `TopologyCanvas`
- [x] `colors.ts` · `layout.ts` · Inspectors
- [x] `npm test` layout port binding — **2 passed**
- [x] `PUT /api/topology/layout` unknown id → **400**
- [x] `TopologyService` validates endpoints / saves layout atomically
- [x] `graph.py` + `test_graph.py` — **4 passed**
- [x] Lab device configs `lab/configs/{r1,sw1,sw2}.cfg` + netplan refs
- [ ] Live EVE traceroute / CDP / `show policy-map` — INFRA deferred (no EVE on this machine)
- [x] Tag `day-02`
- [x] GET `/api/topology` (nodes+speed+services+healthy) · PUT layout 400 · GET device 404
- [x] lifespan `app.state.topology = TopologyService()` fail-fast

## Notes
Map stays LTR (`dir="ltr"` on canvas). Port names only from `topology.json`.
