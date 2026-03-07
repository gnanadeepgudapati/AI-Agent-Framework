# api/chat_routes.py
# Defines all the HTTP endpoints for the chat interface.
# The actual agent logic lives in agent_core.py — these routes
# are just the HTTP layer that sits in front of it.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agent.agent_core import run_agent
from agent.memory_manager import get_history, clear_session

router = APIRouter()


# Request body shape — what the frontend sends us
class ChatRequest(BaseModel):
    session_id: str
    message: str


# Response body shape — what we send back
class ChatResponse(BaseModel):
    session_id: str
    reply: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Receives a message, runs it through the agent, returns the reply.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    reply = run_agent(request.session_id, request.message)

    return ChatResponse(session_id=request.session_id, reply=reply)


@router.get("/{session_id}/history")
async def get_chat_history(session_id: str):
    """
    Returns the full conversation history for a session.
    Useful for the frontend to reload a conversation.
    """
    history = get_history(session_id)

    # Convert LangChain message objects to plain dicts for JSON response
    return {
        "session_id": session_id,
        "history": [
            {
                "role": "human" if msg.__class__.__name__ == "HumanMessage" else "ai",
                "content": msg.content
            }
            for msg in history
        ]
    }


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """
    Clears a session's conversation history.
    Called when the user starts a fresh conversation.
    """
    clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}