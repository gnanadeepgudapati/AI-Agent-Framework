// services/api_client.js
// Handles all communication with the FastAPI backend.
// One function per endpoint — clean and simple.

const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessage(sessionId, message) {
  const response = await fetch(`${BASE_URL}/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  const data = await response.json();
  return data.reply;
}

export async function getChatHistory(sessionId) {
  const response = await fetch(`${BASE_URL}/chat/${sessionId}/history`);

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  return response.json();
}

export async function clearSession(sessionId) {
  const response = await fetch(`${BASE_URL}/chat/${sessionId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  return response.json();
}