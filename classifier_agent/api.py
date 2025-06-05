from fastapi import FastAPI, Request, APIRouter
from pydantic import BaseModel
from classifier_agent.agent import classify_input

router1 = APIRouter()

class ClassificationInput(BaseModel):
    text: str
    # source: str  # email / json / pdf

@router1.post("/classify")
def classify(data: ClassificationInput):
    result = classify_input(data.text)
    print(result)
    return result


