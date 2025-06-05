from fastapi import FastAPI, Request
from pydantic import BaseModel
from shared_memory.memory import SharedMemory
from classifier_agent.agent import classify_input
from email_agent.api import process_email
# from json_agent import ...
# from pdf_agent import ...
from email_agent.api import router as email_router
from classifier_agent.api import router1 as classifier_router

from pdf_agent.agent import PDFAgent

from json_agent.agent import JsonAgent

app = FastAPI()
memory = SharedMemory()
app.include_router(email_router, prefix="/agent")
app.include_router(classifier_router, prefix="/classifer")
class InputRequest(BaseModel):
    entry_id: str  # or UUID if you want stricter validation
    input_text: str

@app.post("/process")
async def process_input(req: InputRequest):
    input_text = req.input_text
    entry_id = req.entry_id

    # Step 1: Classifier Agent
    result = classify_input(input_text)
    format_ = result.get("format")
    intent = result.get("intent")
    trace = result.get("trace")
    print("final_rsult")
    print(result)
    print(format_)
    print(intent)
    # Step 2: Store classification
    classification_data = {
        "entry_id":entry_id,
        "input_source":format_,
        "format":format_,
        "intent":intent,
        "trace":trace
    }
    # memory.write(classification_data)
    memory.write(        
        entry_id=entry_id,
        input_source=format_,
        format=format_,
        intent=intent,
        trace=trace
    )
    # Step 3: Route to appropriate agent
    if format_ == "Email":
        input_final={
            "entry_id": entry_id,
            "email_text":input_text,
        }
        email_data = process_email(input_final)
        print(email_data)

    elif format_ == "JSON":
        json_agent=JsonAgent()
        # print(input_text)
        json_agent.run(entry_id,input_text)

    elif format_ == "PDF":
        pdf_agent=PDFAgent()
        extracted = pdf_agent.run(entry_id, input_text)
        print(f"[Main] PDF Agent Result: {extracted}")

    # print({
    #     "entry_id": entry_id,
    #     "classification": classification_data,
    #     "agent_result": email_data if format_ == "Email" else "handled"
    # })
    return {
        "entry_id": entry_id,
        "classification": classification_data,
        "agent_result": email_data if format_ == "Email" else "handled"
    }
