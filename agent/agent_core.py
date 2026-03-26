# agent/agent_core.py
# The core agent loop. Uses LangGraph's prebuilt ReAct agent
# to route queries through tools and maintain conversation history.

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.memory_manager import get_history, add_message
from agent.tool_registry import get_all_tools

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2,
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
Always use the available tools to fetch real data — never guess or make up answers.
"""


def run_agent(session_id: str, user_message: str) -> str:
    """
    Main entry point for the agent.
    Uses LangGraph's prebuilt ReAct agent for tool calling.
    """
    # Step 1: Save user message
    add_message(session_id, "human", user_message)

    # Step 2: Load tools and create agent
    tools = get_all_tools()
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

    # Step 3: Build message list from history + new input
    history = get_history(session_id)
    # Don't include the message we just added (last item) since
    # we're passing it as part of the invoke call
    past_messages = history[:-1] if history else []
    messages = past_messages + [{"role": "user", "content": user_message}]

    # Step 4: Run the agent
    result = agent.invoke({"messages": messages})

    # Step 5: Extract the final AI response
    ai_reply = result["messages"][-1].content

    # Step 6: Save and return
    add_message(session_id, "ai", ai_reply)
    return ai_reply
