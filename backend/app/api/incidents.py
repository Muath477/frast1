from fastapi import APIRouter, HTTPException, Request

router = APIRouter(tags=["incidents"])


@router.get("/incidents")
def list_incidents(request: Request):
    return request.app.state.incidents.list_incidents()


@router.get("/incidents/{incident_id}")
def get_incident(incident_id: str, request: Request):
    inc = request.app.state.incidents.get(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="incident not found")
    return inc


@router.post("/incidents/{incident_id}/analyze")
async def analyze_incident(incident_id: str, request: Request):
    result = await request.app.state.incidents.analyze(incident_id)
    if result is None:
        raise HTTPException(status_code=404, detail="incident not found or no anomalies")
    return result
