# agent/memory_manager.py
# Manages per-session conversation history for the agent.
# Each session is identified by a unique session_id (UUID from the frontend).

from langchain_core.messages import HumanMessage, AIMessage

# In-memory store: { session_id: [list of messages] }
# NOTE: This resets on server restart. Phase 4 could swap this for Redis.
_sessions: dict = {}


def get_history(session_id: str) -> list:
    """Return message history for a session. Creates empty list if new session."""
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]


def add_message(session_id: str, role: str, content: str) -> None:
    """
    Append a message to session history.
    role must be 'human' or 'ai'.
    """
    history = get_history(session_id)

    if role == "human":
        history.append(HumanMessage(content=content))
    elif role == "ai":
        history.append(AIMessage(content=content))
    else:
        raise ValueError(f"Unknown role: {role}. Use 'human' or 'ai'.")


def clear_session(session_id: str) -> None:
    """Wipe a session's history entirely."""
    if session_id in _sessions:
        del _sessions[session_id]


def get_all_sessions() -> list:
    """Debug helper — returns all active session IDs."""
    return list(_sessions.keys())