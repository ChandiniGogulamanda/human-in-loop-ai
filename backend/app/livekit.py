# backend/app/livekit.py
import os
from dotenv import load_dotenv
from livekit.api import AccessToken, RoomJoinGrant


load_dotenv()
API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")
ROOM_NAME = "salon-room"

def generate_token(identity: str, room_name: str = ROOM_NAME) -> str:
    """
    Generates a JWT token for a participant to join the room.
    """
    grant = RoomJoinGrant(room=room_name)  # <-- use VideoGrants instead of RoomGrant
    token = AccessToken(API_KEY, API_SECRET, identity=identity)
    token.add_grant(RoomJoinGrant(room=room_name))
    return token.to_jwt()


def create_room(room_name: str):
    """
    Placeholder: rooms auto-created when participant joins.
    """
    print(f"Room '{room_name}' will be created automatically when a participant joins.")
    return room_name
