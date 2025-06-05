# email_agent/agent.py
import uuid
import requests
from shared_memory import memory as mem
from email_agent import prompts
from groq import Groq


client = Groq(api_key="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")

class EmailAgent:
    def __init__(self):
        self.name = "EmailAgent"

    def run(self, entry_id: str, email_text: str):
        prompt = prompts.build_email_prompt(email_text)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mistral-saba-24b"
        )
        output = response.choices[0].message.content
        print("[EmailAgent] LLM Output:", output)

        # Very simple extraction
        lines = output.strip().splitlines()
        extracted = {k.lower(): v.strip() for k, v in (
            line.split(":", 1) for line in lines if ":" in line
        )}
        print(45*'*')
        print("extracted_text")
        print(extracted)
        print(45*'*')
        tone = extracted.get("tone", "unknown").lower()
        urgency = extracted.get("urgency", "low").lower()

        trace = [f"EmailAgent → tone: {tone}", f"EmailAgent → urgency: {urgency}"]
        action = None

        if tone in ["angry", "threatening"] or urgency == "high":
            action = "POST /crm/escalate"
            # Simulate POST
            requests.post(
            "http://localhost:9001/crm/escalate",
            json={
                "entry_id": entry_id,
                "sender": extracted.get("sender", "unknown"),
                "issue": extracted.get("issue", "not specified"),
                "urgency": urgency,
                "tone": tone
            }
        )
            trace.append("EmailAgent → triggered escalation")
        
        else:
            action = "LOG_CLOSED"
            trace.append("EmailAgent → logged and closed")
        memory=mem.SharedMemory()
        print(100*'*')
        print(memory)

        memory[entry_id]["email"] = {
            "tone": tone,
            "urgency": urgency,
            "issue": extracted.get("issue", "not specified"),
            "action": action
        }
        memory[entry_id]["trace"].extend(trace)
        
        return {"tone": tone, "urgency": urgency, "action": action, "trace": trace}
