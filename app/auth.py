import uuid
import time

SESSION_STORE = {}

SESSION_TIMEOUT = 3600 

def create_session(user_id: str) -> str:
    token = str(uuid.uuid4())
    SESSION_STORE[token] = {"user_id": user_id, "expires": time.time() + SESSION_TIMEOUT}
    return token

def get_session(token: str) -> dict:
    session = SESSION_STORE.get(token)
    if session and session["expires"] > time.time():
        return session
    return {}
