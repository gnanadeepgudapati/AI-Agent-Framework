# api/agent_server.py
# The FastAPI application entry point.
# This is what uvicorn runs when you start the server.
# It creates the app, adds middleware, and connects the routes.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat_routes import router

app = FastAPI(
    title="AI Agent Framework",
    description="Enterprise assistant that routes queries to HR, IT, and Facilities",
    version="1.0.0"
)

# CORS middleware — allows the React frontend (running on a different port)
# to talk to this backend without the browser blocking the request.
# In production you'd replace "*" with your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all chat routes under the /chat prefix
app.include_router(router, prefix="/chat")


@app.get("/")
def health_check():
    """Basic health check — confirms the server is running."""
    return {"status": "ok", "message": "Agent is live"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.agent_server:app", host="0.0.0.0", port=8000, reload=True)
