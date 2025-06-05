# crm_simulator/main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class EscalationRequest(BaseModel):
    entry_id: str
    sender: str = "unknown"
    issue: str = "unspecified"
    urgency: str = "low"
    tone: str = "neutral"

@app.post("/crm/escalate")
async def escalate_ticket(req: EscalationRequest):
    # Simulate escalation action
    print(f"\n🚨 Escalation Triggered for Entry ID: {req.entry_id}")
    print(f"Sender   : {req.sender}")
    print(f"Issue    : {req.issue}")
    print(f"Urgency  : {req.urgency}")
    print(f"Tone     : {req.tone}")
    return {"status": "escalated", "entry_id": req.entry_id}
