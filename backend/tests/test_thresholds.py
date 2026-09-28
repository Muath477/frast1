from app.intelligence.thresholds import static_severity


def test_link_utilization_normal():
    assert static_severity("link_utilization", 40) == 0.0


def test_link_utilization_warning():
    assert static_severity("link_utilization", 75) == 0.5


def test_link_utilization_critical():
    assert static_severity("link_utilization", 90) == 1.0


def test_dns_success_rate_normal():
    assert static_severity("dns_success_rate", 99) == 0.0


def test_dns_success_rate_warning():
    assert static_severity("dns_success_rate", 80) == 0.5


def test_dns_success_rate_critical():
    assert static_severity("dns_success_rate", 40) == 1.0


def test_unknown_metric():
    assert static_severity("unknown_metric", 999) == 0.0
