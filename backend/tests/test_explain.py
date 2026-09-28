import json
import re

from app.intelligence.explain import grounded, template


def test_grounded_accepts_known_number():
    assert grounded("util 97%", {"util": 97})


def test_grounded_rejects_unknown_number():
    assert not grounded("util 99%", {"util": 97})


def test_arabic_template_has_no_braces():
    out = template(
        "link",
        {
            "label": "R1 Gi0/0",
            "conf": 90,
            "util": 97,
            "speed": 10,
            "lat0": 3,
            "lat": 86,
            "lead": 6,
            "n": 2,
        },
    )
    assert "{" not in out["ar"] and "}" not in out["ar"]
    assert re.search(r"\d", out["ar"])
