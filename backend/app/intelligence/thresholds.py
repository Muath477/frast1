# (warning, critical, direction)  direction: "up" = higher is worse, "down" = lower is worse
THRESHOLDS: dict[str, tuple[float, float, str]] = {
    "link_utilization": (70, 85, "up"),
    "link_latency_ms": (30, 60, "up"),
    "link_packet_loss": (1, 5, "up"),
    "if_out_discards_rate": (5, 50, "up"),
    "if_oper_status": (0.5, 0.5, "down"),
    "cpu_percent": (80, 95, "up"),
    "mem_percent": (85, 95, "up"),
    "http_latency_ms": (300, 1000, "up"),
    "http_ok": (0.5, 0.5, "down"),
    "dns_success_rate": (95, 50, "down"),
    "dns_latency_ms": (100, 500, "up"),
    "poll_timeout": (0.5, 0.5, "up"),
    "syslog_link_down": (0.5, 0.5, "up"),
}


def static_severity(metric: str, value: float) -> float:
    """0 = normal, 0.5 = warning, 1.0 = critical"""
    if metric not in THRESHOLDS:
        return 0.0
    warn, crit, direction = THRESHOLDS[metric]
    if direction == "up":
        return 1.0 if value >= crit else 0.5 if value >= warn else 0.0
    return 1.0 if value <= crit else 0.5 if value < warn else 0.0
