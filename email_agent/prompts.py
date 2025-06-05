# email_agent/prompts.py

def build_email_prompt(email_text: str) -> str:
    return f"""You are an expert email interpreter. Given an email, extract the following:

- Tone: angry, polite, neutral, threatening
- Urgency: high, medium, low
- Issue: summarize in 1 line
- Sender: sender name
Email:
\"\"\"
{email_text}
\"\"\"

Respond with:
Tone: ...
Urgency: ...
Issue: ...
Sender: ...
"""
