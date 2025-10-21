# backend/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .ai_agent import AIAgent
from .knowledge_base import KnowledgeBase
from .db import RequestDB
from .livekit import create_room, generate_token

app = FastAPI(title="Human-in-the-Loop AI System")

# ------------------------------
# Initialize main components
# ------------------------------
agent = AIAgent()
kb = KnowledgeBase()
db = RequestDB()

# ------------------------------
# Setup LiveKit room for AI
# ------------------------------
LIVEKIT_ROOM = "salon-room"
livekit_room = create_room(LIVEKIT_ROOM)
ai_token = generate_token(identity="AI_AGENT", room_name=LIVEKIT_ROOM)
print(f"AI Agent joined LiveKit room '{LIVEKIT_ROOM}' with token: {ai_token}")

# ------------------------------
# Data Models
# ------------------------------
class CallRequest(BaseModel):
    customer_id: str
    question: str

class SupervisorAnswer(BaseModel):
    request_id: int
    answer: str

# ------------------------------
# Root route
# ------------------------------
@app.get("/")
def read_root():
    return {"message": "Human-in-the-Loop AI system is running!"}

# ------------------------------
# 1️⃣ Customer calls AI (HTTP fallback)
# ------------------------------
@app.post("/call")
def receive_call(request: CallRequest):
    """
    The customer asks a question.
    If the AI knows the answer → return it.
    If not → mark as pending and notify supervisor.
    """
    response = agent.handle_query(request.question, participant_id=request.customer_id)

    if response["status"] == "answered":
        return {"status": "answered", "answer": response["answer"]}

    # Store pending request if AI doesn't know the answer
    request_id = db.add_request(request.question, request.customer_id)
    print(f"Supervisor notified: Request {request_id} needs help")

    return {
        "status": "pending",
        "request_id": request_id,
        "message": "Let me check with my supervisor and get back to you."
    }

# ------------------------------
# 2️⃣ Supervisor checks pending questions
# ------------------------------
@app.get("/pending_requests")
def get_pending_requests():
    """
    View all customer questions that the AI could not answer.
    """
    return db.get_pending()

# ------------------------------
# 3️⃣ Supervisor teaches AI the correct answer
# ------------------------------
@app.post("/resolve_request")
def resolve_request(data: SupervisorAnswer):
    """
    Human supervisor provides an answer for a pending question.
    The AI learns it and notifies the customer via LiveKit.
    """
    pending = db.get_request_by_id(data.request_id)
    if not pending:
        raise HTTPException(status_code=404, detail="Request not found")

    question = pending[1]      # column 1 = question text
    customer_id = pending[2]   # column 2 = customer_id

    # Teach AI and save to KB
    kb.learn_answer(question, data.answer)
    agent.learn_from_human(question, data.answer)
    db.resolve_request(data.request_id)

    # Notify customer via LiveKit
    agent.send_livekit_message(customer_id, data.answer)

    print(f"AI learned answer for: '{question}'")
    print(f"Notifying customer ({customer_id}) with: '{data.answer}'")

    return {
        "status": "resolved",
        "message": f"AI has learned and notified the customer: {data.answer}"
    }

# ------------------------------
# TODO: Add WebSocket / LiveKit event listener
# ------------------------------
# - Listen to LiveKit data channel messages from customers
# - Call agent.handle_query() on incoming messages
# - Send responses back via agent.send_livekit_message()
