# json_agent/agent.py
import json,requests,re
from groq import Groq
from shared_memory import memory as mem
from json_agent import prompts

client = Groq(api_key="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")

class JsonAgent:
    def __init__(self):
        self.name = "JsonAgent"

    def run(self, entry_id: str, json_text: str):
        try:
            print("json text")
            print(json_text)
            def fix_to_json(s):
                s = re.sub(r'([{,]\s*)(\w+)\s*:', r'\1"\2":', s)  # keys
                s = re.sub(r':\s*([^",{}]+)', r': "\1"', s)       # values (if not already quoted)
                return s
            json_text=fix_to_json(json_text)
            print(json_text)
            parsed_data = json.loads(json_text)
        except json.JSONDecodeError:
            print("[JsonAgent] Invalid JSON format.")
            return

        prompt = prompts.build_json_prompt(parsed_data)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mistral-saba-24b"
        )
        output = response.choices[0].message.content
        print("[JsonAgent] LLM Output:", output)

        lines = output.strip().splitlines()
        extracted = {k.lower(): v.strip() for k, v in (line.split(":", 1) for line in lines if ":" in line)}
        tone = extracted.get("tone", "neutral")
        urgency = extracted.get("urgency", "low")
        issue = extracted.get("issue", "not specified")

        trace = [f"JsonAgent → tone: {tone}", f"JsonAgent → urgency: {urgency}"]
        action = None

        if tone in ["angry", "threatening"] or urgency == "high":
            action = "POST /crm/escalate"
            requests.post("http://localhost:9000/crm/escalate", json={"entry_id": entry_id})
            trace.append("JsonAgent → triggered escalation")
        else:
            action = "LOG_CLOSED"
            trace.append("JsonAgent → logged and closed")

        memory = mem.SharedMemory()
        memory[entry_id]["json"] = {
            "tone": tone,
            "urgency": urgency,
            "issue": issue,
            "action": action
        }
        memory[entry_id]["trace"].extend(trace)
