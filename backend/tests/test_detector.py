from app.intelligence.detector import Detector


def test_spike_emits_one_raw_alert_and_anomaly():
    d = Detector()
    for i in range(30):
        d.observe("link-r1-sw1", "link_utilization", 14.0, float(i))
    anomaly, raw = d.observe("link-r1-sw1", "link_utilization", 97.0, 30.0)
    assert raw == 1.0
    assert anomaly is not None
    assert anomaly.entity_id == "link-r1-sw1"


def test_repeated_spike_no_extra_alerts():
    d = Detector()
    for i in range(30):
        d.observe("link-r1-sw1", "link_utilization", 14.0, float(i))
    d.observe("link-r1-sw1", "link_utilization", 97.0, 30.0)
    extras = []
    for i in range(10):
        _, raw = d.observe("link-r1-sw1", "link_utilization", 97.0, 31.0 + i)
        extras.append(raw)
    assert all(r is None for r in extras)


def test_recovery_clears_active():
    d = Detector()
    for i in range(30):
        d.observe("link-r1-sw1", "link_utilization", 14.0, float(i))
    d.observe("link-r1-sw1", "link_utilization", 97.0, 30.0)
    assert d.active
    for i in range(16):
        d.observe("link-r1-sw1", "link_utilization", 14.0, 40.0 + i)
    assert not d.active
