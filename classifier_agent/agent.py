from groq import Groq
from uuid import uuid4
from shared_memory import memory
from classifier_agent.prompt_templates import build_few_shot_prompt
import os,re
from dotenv import load_dotenv
load_dotenv()

# /print(GROQ_API_KEY)
client = Groq(api_key="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" )

memory = memory.SharedMemory()

def classify_input(input_text: str):
    prompt = build_few_shot_prompt(input_text)
    # print(prompt)/")
    response = client.chat.completions.create(
        model="mistral-saba-24b",  # or mistral-7b, llama3-8b
        messages=[
            {"role": "system", "content": "You are an expert in identifying file formats and business intent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=100
    )

          
    content = response.choices[0].message.content

    # Extract Format
    # print(content)
    format_match = re.search(r"Format:\s*(\w+)", content)
    intent_match = re.search(r"Intent:\s*(\w+)", content)

    fmt = format_match.group(1) if format_match else None
    intent = intent_match.group(1) if intent_match else None

    print("Format:", fmt)
    print("Intent:", intent)

    print("\n\n")
    entry_id = f"{uuid4().hex[:8]}"
    trace = [
        f"ClassifierAgent → format: {fmt}",
        f"ClassifierAgent → intent: {intent}"
    ]

    # memory.write(
    #     entry_id=entry_id,
    #     input_source=fmt,
    #     format=fmt,
    #     intent=intent,
    #     trace=trace
    # )

    return {
        "entry_id": entry_id,
        "format": fmt,
        "intent": intent,
        "trace": trace
    }
