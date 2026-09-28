# Risk register — trigger → action (Appendix ج)

Use this when an early-warning signal fires. Decision deadlines are from the original plan; for venue day treat remaining open risks as **immediate failover** (`docs/REHEARSAL.md`).

| Risk | Early warning | Action | Decision by |
|---|---|---|---|
| EVE-NG cannot carry load | Nodes take **> 5 min** to boot **or** host CPU **> 90%** | Cut switch RAM, replace vIOS-L2 with Linux bridge, or stronger host | End of Day 2 |
| SNMP returns no numbers | `snmpget` fails | Netmiko `show interfaces` + parse as fallback | End of Day 4 |
| Congestion without clear latency | Hop delta **&lt; 20 ms** | Lower shaper to **5M** or raise iperf to **25M** | Day 5 |
| RCA wrong on a scenario | Top-1 ≠ expected on any run | Tune weights/thresholds + add fixture test | Day 9 |
| UI sluggish | **&lt; 30 FPS** during incident | Cap WS updates **1 Hz**, `React.memo` nodes, disable animation on healthy links | Day 10 |
| LLM slow / offline | **> 4 s** | Template is primary — set `LLM_ENABLED=0` on demo day unless net is sure | Day 11 |
| Overall schedule slip | Milestone **M2** missed end of Day 7 | Activate **7-day compressed plan** from Day 8 (`docs/COMPRESSED_PLANS.md`): drop Replay, Isolation Forest, Arabic | Day 7 |

## Status on this build (sim-first)

| Risk | Status |
|---|---|
| EVE load | Venue / INFRA — golden snapshot documented in README |
| SNMP | Live path; sim uses in-process metrics |
| Congestion latency | Sim scenario targets designed for visible delta |
| RCA | Day 12 measure: Top-1 **9/9** |
| UI FPS | Sim E2E ×3 green; throttle if venue display stutters |
| LLM | Template-first; disable for pitch if unsure |
| Schedule | Full 14-day path completed → tags through `day-14` / `v1.0` |
