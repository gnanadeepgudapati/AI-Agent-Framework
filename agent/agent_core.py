# agent/agent_core.py
# The core agent loop. Takes a user message, runs it through GPT-4o with
# conversation history, returns the response. Tools get added in Phase 2.

# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage

# from agent.memory_manager import get_history, add_message

# load_dotenv()

# # Initialize the LLM once at module level — no need to recreate it per request
# llm = ChatOpenAI(
# model=os.getenv("OPENAI_MODEL", "gpt-4o"),
# api_key=os.getenv("OPENAI_API_KEY"),
# temperature=0.2,  # low temperature = consistent, predictable routing
# )

# SYSTEM_PROMPT = """You are an intelligent enterprise assistant. 
# You help employees with HR, IT, and Facilities requests.
# Be concise, professional, and always clarify which system you are 
# routing their request to.

# Current available domains:
# - HR: leave balance, payroll, personal info
# - IT: tickets, password resets, software requests  
# - Facilities: room bookings, maintenance, parking

# If a query doesn't belong to any domain, say so clearly.
# """


# def run_agent(session_id: str, user_message: str) -> str:
# """
# Main entry point for the agent.
# Loads history, runs the LLM, saves response, returns answer.
# """
# # Step 1: Save the user's message to history
# add_message(session_id, "human", user_message)

# # Step 2: Build the full message list — system prompt + history
# history = get_history(session_id)
# messages = [SystemMessage(content=SYSTEM_PROMPT)] + history

# # Step 3: Call the LLM
# response = llm.invoke(messages)

# # Step 4: Save the AI response to history
# ai_reply = response.content
# add_message(session_id, "ai", ai_reply)

# return ai_reply


import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor



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

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def run_agent(session_id: str, user_message: str) -> str:
    """
    Main entry point for the agent.
    Uses LangChain's create_tool_calling_agent for proper tool execution.
    """
    #Step 1: Save user message
    add_message(session_id, "human", user_message )
    
    # Step 2: Load tools
    tools = get_all_tools()

    # Step 3: Create agent and executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

     # Step 4: Get history and run
    history = get_history(session_id)
    result = executor.invoke({
        "input": user_message,
        "chat_history": history,
    })

    ai_reply = result["output"]

    # Step 5: Save and return
    add_message(session_id, "ai", ai_reply)
    return ai_reply