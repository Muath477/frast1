import json
import re

import httpx

from app.core.config import settings

TEMPLATES = {
    "link": {
        "en": (
            "Most likely cause: congestion on {label} ({conf}% confidence). Utilization reached {util}% of a "
            "{speed} Mbps link and latency rose from {lat0} ms to {lat} ms, starting {lead}s before the "
            "service symptoms. {n} affected service(s) sit downstream of this link."
        ),
        "ar": (
            "السبب الأرجح: ازدحام على الرابط {label} بثقة {conf}%. وصل الاستخدام إلى {util}% من سعة {speed} Mbps "
            "وارتفع زمن التأخير من {lat0} ms إلى {lat} ms، وبدأ ذلك قبل أعراض الخدمات بـ{lead} ثانية. "
            "عدد الخدمات المتأثرة الواقعة خلف هذا الرابط: {n}."
        ),
    },
    "svc-dns": {
        "en": (
            "Most likely cause: DNS failure on {label} ({conf}% confidence). Success rate dropped to {dns}% "
            "and latency rose to {dnsLat} ms. {n} dependent service(s) failed afterward."
        ),
        "ar": (
            "السبب الأرجح: فشل خدمة DNS على {label} بثقة {conf}%. انخفضت نسبة النجاح إلى {dns}% "
            "وارتفع زمن الاستجابة إلى {dnsLat} ms. عدد الخدمات المعتمدة التي فشلت لاحقًا: {n}."
        ),
    },
    "server": {
        "en": (
            "Most likely cause: resource pressure on {label} ({conf}% confidence). CPU reached {cpu}% "
            "and service latency rose to {http} ms. {n} service(s) hosted here are affected."
        ),
        "ar": (
            "السبب الأرجح: ضغط موارد على {label} بثقة {conf}%. وصل المعالج إلى {cpu}% "
            "وارتفع زمن الخدمة إلى {http} ms. عدد الخدمات المستضافة المتأثرة: {n}."
        ),
    },
}

NUM = re.compile(r"\d+(?:\.\d+)?")


def grounded(text: str, facts: dict) -> bool:
    """Reject any number in the text that is not in measured facts — anti-hallucination guard."""
    norm = lambda n: f"{float(n):g}"
    allowed = {norm(n) for n in NUM.findall(json.dumps(facts))}
    return all(norm(n) in allowed for n in NUM.findall(text))


def template(kind: str, facts: dict) -> dict:
    t = TEMPLATES[kind]
    return {"en": t["en"].format(**facts), "ar": t["ar"].format(**facts), "source": "template"}


async def explain(kind: str, facts: dict) -> dict:
    base = template(kind, facts)
    if not settings.llm_enabled or not settings.anthropic_api_key:
        return base
    prompt = (
        "Rewrite this incident explanation for a NOC engineer in 2 short sentences. Use ONLY the facts in the "
        f"JSON; do not add any number that is not in it. Use Western digits.\nFACTS: {json.dumps(facts)}\n"
        f"DRAFT: {base['en']}"
    )
    try:
        async with httpx.AsyncClient(timeout=4.0) as c:
            r = await c.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": settings.llm_model,
                    "max_tokens": 200,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            r.raise_for_status()
            text = "".join(b.get("text", "") for b in r.json()["content"])
        if grounded(text, facts):
            return {**base, "en": text.strip(), "source": "llm"}
    except Exception:
        pass
    return base
