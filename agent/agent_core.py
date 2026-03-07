# agent/agent_core.py
# The core agent loop. Takes a user message, runs it through GPT-4o with
# conversation history, returns the response. Tools get added in Phase 2.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from agent.memory_manager import get_history, add_message

load_dotenv()

# Initialize the LLM once at module level — no need to recreate it per request
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2,  # low temperature = consistent, predictable routing
)

SYSTEM_PROMPT = """You are an intelligent enterprise assistant. 
You help employees with HR, IT, and Facilities requests.
Be concise, professional, and always clarify which system you are 
routing their request to.

Current available domains:
- HR: leave balance, payroll, personal info
- IT: tickets, password resets, software requests  
- Facilities: room bookings, maintenance, parking

If a query doesn't belong to any domain, say so clearly.
"""


def run_agent(session_id: str, user_message: str) -> str:
    """
    Main entry point for the agent.
    Loads history, runs the LLM, saves response, returns answer.
    """
    # Step 1: Save the user's message to history
    add_message(session_id, "human", user_message)

    # Step 2: Build the full message list — system prompt + history
    history = get_history(session_id)
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + history

    # Step 3: Call the LLM
    response = llm.invoke(messages)

    # Step 4: Save the AI response to history
    ai_reply = response.content
    add_message(session_id, "ai", ai_reply)

    return ai_reply