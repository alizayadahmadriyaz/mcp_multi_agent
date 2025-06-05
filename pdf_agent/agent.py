# pdf_agent/agent.py
import os
import fitz  # PyMuPDF
from groq import Groq
from shared_memory import memory as mem
import re

client = Groq(api_key="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")

class PDFAgent:
    def __init__(self):
        self.name = "PDFAgent"

    def run(self, entry_id: str, pdf_path: str):
        # Load PDF text
        text = self.extract_text(pdf_path)
        print(text)
        if not text:
            return {"error": "Empty PDF or unreadable."}

        # Call LLM to analyze the PDF content
        llm_response = self.analyze_with_llm(text[:3000])  # Limit size to avoid overrun
        print("[PDFAgent] LLM Output:", llm_response)

        # Try to parse response into key fields
        extracted = self.parse_llm_response(llm_response)
        trace = [f"PDFAgent → LLM analysis complete"]

        # Escalation check (optional trigger)
        action = "LOG_CLOSED"
        if extracted.get("urgency") == "high":
            action = "POST /crm/escalate"
            trace.append("PDFAgent → triggered escalation")
        else:
            trace.append("PDFAgent → logged and closed")

        # Save to memory
        memory = mem.SharedMemory()
        memory[entry_id]["pdf"] = extracted
        memory[entry_id]["trace"].extend(trace)

        return {"action": action, "extracted": extracted, "trace": trace}

    def extract_text(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            return "\n".join(page.get_text() for page in doc)
        except Exception as e:
            print(f"[PDFAgent] PDF Extraction Error: {e}")
            return ""

    def analyze_with_llm(self, text):
        prompt = f"""
        Analyze the following PDF text and extract:
        - format
        - tone
        - urgency (low, medium, high)
        - key issue

        Respond in the format:
        Format: <format>
        Tone: <tone>
        Urgency: <urgency>
        Issue: <issue>

        TEXT:
        {text}
        """
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def parse_llm_response(self, response):
        lines = response.strip().splitlines()
        return {
            k.lower(): v.strip()
            for line in lines if ":" in line
            for k, v in [line.split(":", 1)]
        }
