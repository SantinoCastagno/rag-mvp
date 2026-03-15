# API Protocol

## Overview

- **Style:** REST over HTTP
- **Base URL:** `http://localhost:8000`
- **Authentication:** None (POC — no auth layer)
- **Interactive docs:** `http://localhost:8000/docs` (Swagger UI)
- **Common response format:** JSON. Errors follow FastAPI's default `{"detail": "..."}` envelope.

---

## Endpoints

### Health Check

#### `GET /`

Returns a liveness message.

**Response `200`**
```json
{
  "message": "Basic RAG API with Gemini 2.5 Flash-Lite"
}
```

---

### Documents

#### `POST /ingest`

Uploads and ingests a file into the vector store. The file is split into chunks, embedded, and stored in ChromaDB.

**Request**

`Content-Type: multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | A `.pdf` or `.md` file |

**Response `200`**
```json
{
  "message": "Successfully ingested report.pdf",
  "chunks": 42
}
```

**Error responses**

| Status | When |
|--------|------|
| `400` | File extension is not `.pdf` or `.md` |
| `500` | Loading, splitting, or embedding failed |

---

### Chat

#### `POST /chat`

Sends a question and receives an answer grounded in the ingested documents. Chat history for the session is automatically loaded and persisted.

**Request body**

```json
{
  "question": "What are the main conclusions of the document?",
  "session_id": "3f7a1c2e-84b0-4e2a-9d3f-1c2e3f4a5b6c"
}
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `question` | `string` | min=1, max=2000 | The user's question |
| `session_id` | `string` | min=1, max=100 | Session identifier (any stable string, typically a UUID) |

**Response `200`**
```json
{
  "answer": "The document concludes that...",
  "sources": ["report.pdf", "notes.md"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `answer` | `string` | LLM-generated answer |
| `sources` | `string[]` | Deduplicated list of source filenames for retrieved chunks |

**Error responses**

| Status | When |
|--------|------|
| `422` | Request body fails validation (e.g. empty question) |
| `500` | RAG chain or LLM invocation failed |

---

### History

#### `GET /history/{session_id}`

Returns the full conversation history for a session.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | `string` | The session identifier |

**Response `200`**
```json
[
  { "role": "user", "content": "What is this document about?" },
  { "role": "assistant", "content": "This document is about..." }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `role` | `string` | `"user"` or `"assistant"` |
| `content` | `string` | Message text |

Returns an empty array `[]` if no history exists for the session.

**Error responses**

| Status | When |
|--------|------|
| `500` | SQLite read failed |
