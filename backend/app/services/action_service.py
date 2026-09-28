from datetime import datetime, timezone
from itertools import count

from app.services.hub import hub

RECOMMENDATIONS = {
    "link": {
        "actionType": "apply_qos_policy",
        "risk": "low",
        "scenario": "uplink-congestion",
        "description": (
            "Apply UPLINK-QOS on R1 Gi0/0: police bulk traffic (port 5201) to 2 Mbps "
            "and fair-queue critical flows."
        ),
        "alternatives": ["Activate an alternate path", "Increase uplink capacity"],
    },
    "svc-dns": {
        "actionType": "restart_dns_service",
        "risk": "low",
        "scenario": "dns-failure",
        "description": "Restart the 'named' DNS service on APP-01.",
        "alternatives": ["Fail over to secondary DNS"],
    },
    "server": {
        "actionType": "stop_runaway_process",
        "risk": "medium",
        "scenario": "server-spike",
        "description": "Terminate the runaway CPU process on APP-01 (stress-ng).",
        "alternatives": ["Scale out the web tier", "Move workload to standby node"],
    },
}

EXPECTED_ROOT = {
    "uplink-congestion": "link-r1-sw1",
    "dns-failure": "svc-dns",
    "server-spike": "app01",
}


def kind_for_entity(entity_id: str) -> str:
    if entity_id.startswith("link-"):
        return "link"
    if entity_id == "svc-dns":
        return "svc-dns"
    return "server"


class ActionService:
    def __init__(self, incidents, demo_ref, detector, history, simulator_ref, audit):
        self.incidents = incidents
        self.demo_ref = demo_ref
        self.detector = detector
        self.history = history
        self.simulator_ref = simulator_ref  # callable -> Simulator | None
        self.audit = audit
        self.actions: dict[str, dict] = {}
        self.runs: list[dict] = []
        self._seq = count(1)
        self._recovering: dict[str, float] = {}  # incident_id -> clear_since

    def recommend(self, inc) -> dict:
        root = (inc.root_cause or {}).get("entityId") or next(iter(inc.members), "unknown")
        kind = kind_for_entity(root)
        rec = RECOMMENDATIONS[kind]
        aid = f"ACT-{next(self._seq):04d}"
        action = {
            "id": aid,
            "incidentId": inc.id,
            "actionType": rec["actionType"],
            "description": rec["description"],
            "riskLevel": rec["risk"],
            "approvalStatus": "pending",
            "scenario": rec["scenario"],
            "alternatives": rec["alternatives"],
        }
        self.actions[aid] = action
        inc.action = action
        inc.status = "awaiting_approval"
        return action

    async def approve(self, action_id: str, decided_by: str) -> dict:
        action = self.actions.get(action_id)
        if not action:
            raise KeyError(action_id)
        inc = self.incidents.open.get(action["incidentId"])
        if not inc:
            raise KeyError(action["incidentId"])

        now = datetime.now(timezone.utc).isoformat()
        action["approvalStatus"] = "approved"
        action["decidedBy"] = decided_by
        action["decidedAt"] = now
        inc.timings["decidedAt"] = now
        inc.status = "approved"
        inc.action = action
        self.audit.log(decided_by, "approve", action_id, {"incidentId": inc.id})

        demo = self.demo_ref()
        scenario = action.get("scenario") or demo.get("scenario") or "uplink-congestion"
        try:
            if demo.get("mode") == "sim":
                sim = self.simulator_ref()
                if sim:
                    sim.remediate()
            else:
                from app.services import lab_client

                await lab_client.call(f"/remediate/{scenario}")
            action["approvalStatus"] = "executed"
            action["executedAt"] = datetime.now(timezone.utc).isoformat()
            inc.timings["executedAt"] = action["executedAt"]
            inc.status = "approved"  # recovery monitor moves to resolved
            demo["state"] = "remediating"
            await hub.broadcast("demo", demo)
            self.audit.log(decided_by, "execute", action_id, {"scenario": scenario, "ok": True})
        except Exception as e:
            action["approvalStatus"] = "failed"
            self.audit.log(decided_by, "execute_failed", action_id, {"error": str(e)})

        inc.action = action
        if self.incidents.persist:
            self.incidents.persist(inc)
        await hub.broadcast("incident", inc.to_dict())
        return action

    async def reject(self, action_id: str, decided_by: str, reason: str) -> dict:
        if not reason or len(reason.strip()) < 5:
            raise ValueError("reason must be at least 5 characters")
        action = self.actions.get(action_id)
        if not action:
            raise KeyError(action_id)
        inc = self.incidents.open.get(action["incidentId"])
        if not inc:
            raise KeyError(action["incidentId"])

        now = datetime.now(timezone.utc).isoformat()
        action["approvalStatus"] = "rejected"
        action["decidedBy"] = decided_by
        action["reason"] = reason.strip()
        action["decidedAt"] = now
        inc.timings["decidedAt"] = now
        # Stay awaiting_approval with a fresh pending action
        new_action = {
            **{k: v for k, v in action.items() if k not in ("id", "approvalStatus", "decidedBy", "reason", "decidedAt", "executedAt")},
            "id": f"ACT-{next(self._seq):04d}",
            "approvalStatus": "pending",
        }
        self.actions[new_action["id"]] = new_action
        inc.action = new_action
        inc.status = "awaiting_approval"
        self.audit.log(
            decided_by,
            "reject",
            action_id,
            {"incidentId": inc.id, "reason": reason.strip(), "replacement": new_action["id"]},
        )
        if self.incidents.persist:
            self.incidents.persist(inc)
        await hub.broadcast("incident", inc.to_dict())
        return new_action

    async def recovery_tick(self):
        now = datetime.now(timezone.utc).timestamp()
        for inc in list(self.incidents.open.values()):
            action = inc.action or {}
            if action.get("approvalStatus") != "executed":
                continue
            members_clear = all(
                not any(k[0] == m for k in self.detector.active) for m in inc.members
            )
            if members_clear:
                since = self._recovering.get(inc.id)
                if since is None:
                    self._recovering[inc.id] = now
                    continue
                if now - since < 15:
                    continue
                # Resolved
                recovered_at = datetime.now(timezone.utc).isoformat()
                inc.status = "resolved"
                inc.resolved_at = recovered_at
                inc.timings["recoveredAt"] = recovered_at
                root = (inc.root_cause or {}).get("entityId")
                if root:
                    self.history.record(root)
                demo = self.demo_ref()
                demo["state"] = "recovered"
                await hub.broadcast("demo", demo)
                self._record_run(inc, demo)
                self._recovering.pop(inc.id, None)
                self.incidents.history_list.append(inc)
                del self.incidents.open[inc.id]
                if self.incidents.persist:
                    self.incidents.persist(inc)
                await hub.broadcast("incident", inc.to_dict())
                self.audit.log("system", "resolved", inc.id, {"root": root})
            else:
                self._recovering.pop(inc.id, None)

    def _record_run(self, inc, demo: dict):
        def parse(ts: str | None):
            if not ts:
                return None
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()

        t = inc.timings
        inj = parse(t.get("injectedAt"))
        det = parse(t.get("detectedAt"))
        ana = parse(t.get("analyzedAt"))
        rec = parse(t.get("recoveredAt"))
        scenario = demo.get("scenario") or (inc.action or {}).get("scenario")
        root = (inc.root_cause or {}).get("entityId")
        metrics = {
            "timeToDetect": (det - inj) if inj and det else None,
            "timeToRootCause": (ana - inj) if inj and ana else None,
            "timeToRecover": (rec - inj) if inj and rec else None,
            "rawAlerts": inc.raw_alert_count,
            "incidents": 1,
            "noiseReduction": 1 - 1 / max(inc.raw_alert_count, 1),
            "correct": root == EXPECTED_ROOT.get(scenario or "", None),
        }
        self.runs.append(
            {
                "scenario": scenario,
                "mode": demo.get("mode"),
                "incidentId": inc.id,
                "metrics": metrics,
            }
        )
