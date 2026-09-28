# Day 02 — Real topology (ports + custom edges)

## Acceptance
- [x] `DeviceNode` + `PortEdge` + `TopologyCanvas`
- [x] `colors.ts` · `layout.ts` · Inspectors
- [x] `npm test` layout port binding — **2 passed**
- [x] `PUT /api/topology/layout` unknown id → **400**
- [x] `TopologyService` validates endpoints / saves layout atomically
- [x] `graph.py` + `test_graph.py` — **4 passed**
- [x] Lab device configs `lab/configs/{r1,sw1,sw2}.cfg`
- [ ] Live EVE traceroute / CDP — INFRA deferred
- [x] Tag `day-02`

## Notes
Map stays LTR (`dir="ltr"` on canvas). Port names only from `topology.json`.
