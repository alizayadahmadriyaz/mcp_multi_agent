# email_agent/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from  email_agent import agent

router = APIRouter()
agent = agent.EmailAgent()

class EmailInput(BaseModel):
    entry_id: str
    email_text: str

@router.post("/email/process")
def process_email(data: EmailInput):
    print(55*'*')
    print(data)
    return agent.run(data['entry_id'], data['email_text'])
