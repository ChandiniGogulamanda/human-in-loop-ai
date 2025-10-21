# backend/app/ai_agent.py
from .knowledge_base import KnowledgeBase
from .livekit import create_room, generate_token

class AIAgent:
    def __init__(self, room_name="salon-room"):
        # Initialize knowledge base
        self.kb = KnowledgeBase()

        # Setup LiveKit room
        self.room_name = room_name
        self.room = create_room(room_name)

        # Generate AI token for joining the room
        self.token = generate_token(identity="AI_AGENT", room_name=room_name)

        print(f"AI Agent ready in room '{room_name}' with token: {self.token}")

    def handle_query(self, question: str, participant_id: str = None):
        """
        Handle a query coming from a participant.
        If answer exists in KB -> return it.
        Else -> escalate to supervisor.
        participant_id is optional, used for sending back response via LiveKit.
        """
        # Step 1: Try to find answer in KB
        answer = self.kb.get_answer(question)
        if answer:
            print(f"AI Agent: Found answer in KB -> {answer}")
            
            # Send answer via LiveKit if participant_id is provided
            if participant_id:
                self.send_livekit_message(participant_id, answer)
            
            return {"status": "answered", "answer": answer}

        # Step 2: Escalate to human supervisor
        print(f"AI Agent: No answer found for '{question}', escalating to supervisor...")
        # This is where you would add DB pending request creation logic
        return {
            "status": "pending",
            "message": "Let me check with my supervisor and get back to you."
        }

    def learn_from_human(self, question: str, answer: str):
        """
        Learn new answer provided by human supervisor.
        """
        self.kb.learn_answer(question, answer)
        print(f"AI Agent: Learned new answer for '{question}' -> {answer}")
        return {"status": "learned", "message": f"Learned new answer for '{question}'"}

    def send_livekit_message(self, participant_id: str, message: str):
        """
        Placeholder for sending a message via LiveKit data channel.
        Replace this with actual LiveKit SDK integration.
        """
        print(f"Sending message to participant '{participant_id}' in room '{self.room_name}': {message}")
        # Example (pseudo-code):
        # livekit_client.send_data(room=self.room_name, participant_id=participant_id, message=message)
