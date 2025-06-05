import json
def build_json_prompt(data: dict):
    return (
        "You are a business analyst.\n"
        "Analyze the following JSON payload and extract the tone, urgency, and issue description.\n\n"
        f"{json.dumps(data, indent=2)}\n\n"
        "Respond with:\n"
        "Tone: <tone>\n"
        "Urgency: <urgency>\n"
        "Issue: <brief description>"
    )