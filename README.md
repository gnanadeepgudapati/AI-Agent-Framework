# AI Agent Extensibility Framework

A plugin-based stateful agent that intelligently routes enterprise queries to the right service — HR, IT, or Facilities — using LangChain orchestration and OpenAI function calling. One interface, three systems, zero confusion.

---

## What This Does

Employees deal with three completely separate systems for everyday requests — HR for leave, IT for tickets, Facilities for room bookings. Nobody knows which system to use or how. This agent fixes that.

You ask it anything in plain English. It figures out which system the query belongs to, calls the right service plugin, and responds with a real answer. It remembers the conversation so follow-up questions just work.

Example queries it handles:
- "How many vacation days do I have left?"
- "My laptop won't connect to VPN, can you raise a ticket?"
- "Book a meeting room for 10 people this Friday at 2pm"

---

## Architecture

```
User → React Frontend → FastAPI Backend → LangChain Agent → OpenAI Function Calling
                                                          ↓
                                          ┌───────────────────────────┐
                                          │ HRIS Plugin  │ leave, payroll, HR data    │
                                          │ ITSM Plugin  │ tickets, passwords, software│
                                          │ Facilities   │ rooms, maintenance, parking │
                                          └───────────────────────────┘
                                                          ↓
                                              AWS Secrets Manager
                                              Docker + ECR + CI/CD
```

---

## Project Structure

```
AI-Agent-Framework/
│
├── agent/
│   ├── agent_core.py          — LangChain agent setup and conversation loop
│   ├── tool_registry.py       — registers all plugin tools with the agent
│   └── memory_manager.py      — handles conversation state and history
│
├── plugins/
│   ├── base_plugin.py         — base class all plugins inherit from
│   ├── hris_plugin.py         — HR tools: leave, payroll, personal info
│   ├── itsm_plugin.py         — IT tools: tickets, passwords, software requests
│   └── facilities_plugin.py   — Facilities tools: rooms, maintenance, parking
│
├── api/
│   ├── agent_server.py        — FastAPI entry point
│   └── chat_routes.py         — chat endpoints
│
├── frontend/
│   └── agent-ui/              — React application
│       ├── src/
│       │   ├── App.jsx
│       │   ├── components/
│       │   │   ├── ChatWindow.jsx
│       │   │   ├── MessageBubble.jsx
│       │   │   └── ToolCallIndicator.jsx
│       │   └── services/
│       │       └── api_client.js
│       └── package.json
│
├── infrastructure/
│   ├── Dockerfile             — container definition
│   ├── docker-compose.yml     — local multi-service setup
│   └── github-actions/
│       └── deploy.yml         — CI/CD pipeline
│
├── tests/
│   ├── test_agent_core.py
│   ├── test_plugins.py
│   └── test_routing.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## Build Plan

**Phase 1 — Agent Core**
LangChain agent setup, OpenAI function calling, basic conversation memory, FastAPI server running. No plugins yet — just a working agent that can hold a conversation.
- Deliverable: agent that responds to messages and remembers context

**Phase 2 — Service Plugins**
Plugin base class, three domain plugins (HRIS, ITSM, Facilities), query routing working end to end. Agent correctly identifies which plugin to call and returns real data.
- Deliverable: full routing working across all three services

**Phase 3 — React Frontend**
React chat interface, message bubbles, tool call visibility so users can see which service was called, connected to the FastAPI backend.
- Deliverable: working chat UI you can demo

**Phase 4 — AWS + Docker**
Dockerfile, AWS Secrets Manager for API keys, IAM roles, ECR image registry, GitHub Actions CI/CD pipeline that builds and pushes on every commit.
- Deliverable: production-ready, containerized, automated deployment

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python + FastAPI + AsyncIO | Async-ready, fast, production grade |
| Agent | LangChain | Manages agent loop, memory, tool calling |
| LLM | OpenAI GPT-4o | Function calling, best-in-class routing |
| Frontend | React + Tailwind CSS | Component-based, industry standard |
| Containers | Docker | Consistent environments, portable |
| Registry | AWS ECR | Stores Docker images |
| Secrets | AWS Secrets Manager | Secure credential management |
| Auth | AWS IAM | Role-based access control |
| CI/CD | GitHub Actions | Automated build and push pipeline |

---

## Dependencies

```txt
fastapi
uvicorn
pydantic
langchain
langchain-openai
openai
python-dotenv
httpx
boto3
```

Install everything:
```bash
pip install -r requirements.txt
```

---

## Environment Setup

```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o
AWS_REGION=us-east-2
```

---

## Running Locally

**Backend:**
```bash
uvicorn api.agent_server:app --reload
```

**Frontend:**
```bash
cd frontend/agent-ui
npm install
npm run dev
```

**With Docker:**
```bash
docker-compose up --build
```

---

## API Endpoints

- `POST /chat` — send a message to the agent
- `GET /chat/{session_id}/history` — get conversation history
- `DELETE /chat/{session_id}` — clear a session

---

## Current Status

- [x] Repo initialized
- [x] Project structure defined
- [x] Phase 1 — Agent core + FastAPI
- [ ] Phase 2 — Service plugins
- [ ] Phase 3 — React frontend
- [ ] Phase 4 — Docker + AWS + CI/CD
---

## Why This Matters

Enterprise employees waste hours navigating disconnected systems. This project demonstrates a production-grade approach to solving that — a stateful, extensible agent with clean plugin architecture, secure credential management, and automated deployment. The same pattern powers real enterprise AI products.
