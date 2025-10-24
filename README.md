## Human-in-the-Loop AI Agent System

This project implements a Human-in-the-Loop AI Customer Support System.
If the AI cannot answer a user query, it automatically:

✅ Escalates to a human supervisor

✅ Stores the correct response in a knowledge base

✅ Learns and replies automatically next time

# Technology Stack

Backend- API	FastAPI

Communication-	LiveKit

Database-	SQLite

Server Runtime-	Uvicorn

# Installation & Setup

**Clone Repository**

git clone <your-repo-url>

cd human-in-the-loop

**Create Virtual Environment**

python -m venv venv


**Activate:**

**Windows:**

venv\Scripts\activate

**Install Dependencies**

pip install -r requirements.txt


**Verify LiveKit installation:**

python -c "import livekit.api; print('LiveKit OK!')"

**Run FastAPI Server**

uvicorn backend.app.main:app --reload --port 8000
