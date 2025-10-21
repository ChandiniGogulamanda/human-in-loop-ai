# backend/app/supervisor_ui.py
from fastapi import FastAPI
from pydantic import BaseModel
from .db import RequestDB
from .knowledge_base import KnowledgeBase

app = FastAPI()
db = RequestDB()
kb = KnowledgeBase()

class SupervisorAnswer(BaseModel):
    request_id: int
    answer: str

@app.get("/pending_requests")
def pending_requests():
    return db.get_pending()

@app.post("/resolve_request")
def resolve_request(data: SupervisorAnswer):
    # Learn answer in KB
    kb.learn_answer(f"Question_{data.request_id}", data.answer)
    db.resolve_request(data.request_id)
    print(f"AI: Notifying customer of answer: {data.answer}")
    return {"status": "resolved"}
