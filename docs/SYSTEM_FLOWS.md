# System Flows

## Core Flows

### 1. Document Ingestion

```mermaid
sequenceDiagram
    participant User
    participant Streamlit as Streamlit (app/ui/app.py)
    participant API as FastAPI (routes.py)
    participant Ingestion as ingestion.py
    participant Factory as llm_factory.py
    participant Chroma as ChromaDB

    User->>Streamlit: Upload PDF or .md file
    User->>Streamlit: Click "Ingest File"
    Streamlit->>API: POST /ingest (multipart/form-data)
    API->>Ingestion: process_file(content, filename)
    Ingestion->>Ingestion: Write bytes to tempfile
    alt .pdf
        Ingestion->>Ingestion: PyPDFLoader.load()
    else .md
        Ingestion->>Ingestion: TextLoader.load()
    end
    Ingestion->>Ingestion: RecursiveCharacterTextSplitter.split_documents()
    Ingestion->>Factory: get_embeddings()
    Factory-->>Ingestion: Embeddings (Gemini or Ollama)
    Ingestion->>Chroma: add_documents(chunks)
    Chroma-->>Ingestion: OK
    Ingestion->>Ingestion: Remove tempfile
    Ingestion-->>API: num_chunks
    API-->>Streamlit: 200 {"message": "...", "chunks": N}
    Streamlit-->>User: Success toast
```

---

### 2. Chat (RAG Query)

```mermaid
sequenceDiagram
    participant User
    participant Streamlit as Streamlit (app/ui/app.py)
    participant API as FastAPI (routes.py)
    participant RAGChain as rag_chain.py
    participant SQLite as SQLite (chat_history.db)
    participant Chroma as ChromaDB
    participant Factory as llm_factory.py
    participant LLM as LLM (Gemini / Ollama)

    User->>Streamlit: Type question and press Enter
    Streamlit->>API: POST /chat {question, session_id}
    API->>RAGChain: chain.invoke({question}, config={session_id})
    RAGChain->>SQLite: get_session_history(session_id)
    SQLite-->>RAGChain: Previous messages
    RAGChain->>Chroma: retriever.get_relevant_documents(question, k=RETRIEVER_K)
    Chroma-->>RAGChain: Top-K document chunks
    RAGChain->>RAGChain: format_docs(chunks) → context string
    RAGChain->>Factory: get_llm()
    Factory-->>RAGChain: BaseChatModel instance
    RAGChain->>LLM: Invoke prompt (context + chat_history + question)
    LLM-->>RAGChain: Answer text
    RAGChain->>SQLite: Persist HumanMessage + AIMessage
    RAGChain-->>API: {result, source_documents}
    API-->>Streamlit: 200 {answer, sources}
    Streamlit-->>User: Render answer + source filenames
```

---

### 3. Session History Load (on page load)

```mermaid
sequenceDiagram
    participant Streamlit as Streamlit (app/ui/app.py)
    participant API as FastAPI (routes.py)
    participant SQLite as SQLite (chat_history.db)

    Streamlit->>Streamlit: Generate/reuse session_id (uuid4 in st.session_state)
    Streamlit->>API: GET /history/{session_id}
    API->>SQLite: get_session_history(session_id).messages
    SQLite-->>API: List of HumanMessage / AIMessage
    API-->>Streamlit: [{role, content}, ...]
    Streamlit->>Streamlit: Render chat history
```

---

## External Integrations

### Google Gemini API

```mermaid
sequenceDiagram
    participant Factory as llm_factory.py
    participant GeminiLLM as ChatGoogleGenerativeAI
    participant GeminiEmbed as GoogleGenerativeAIEmbeddings
    participant GeminiAPI as Google Gemini API

    Factory->>GeminiLLM: Instantiate (model, api_key, temperature)
    Factory->>GeminiEmbed: Instantiate (model, api_key)
    GeminiLLM->>GeminiAPI: Chat completion request
    GeminiAPI-->>GeminiLLM: Response text
    GeminiEmbed->>GeminiAPI: Embed texts request
    GeminiAPI-->>GeminiEmbed: Embedding vectors
```

Active when `LLM_PROVIDER=gemini`. Requires `GOOGLE_API_KEY`. Default models: `gemini-2.5-flash-lite` (LLM) and `models/text-embedding-004` (embeddings).

### Ollama (Local)

```mermaid
sequenceDiagram
    participant Factory as llm_factory.py
    participant OllamaLLM as ChatOllama
    participant OllamaEmbed as OllamaEmbeddings
    participant OllamaServer as Ollama Server (localhost:11434)

    Factory->>OllamaLLM: Instantiate (model, base_url, temperature)
    Factory->>OllamaEmbed: Instantiate (model, base_url)
    OllamaLLM->>OllamaServer: Chat request
    OllamaServer-->>OllamaLLM: Response text
    OllamaEmbed->>OllamaServer: Embed request
    OllamaServer-->>OllamaEmbed: Embedding vectors
```

Active when `LLM_PROVIDER=ollama`. Requires a running Ollama server. Default models: `mistral` (LLM) and `nomic-embed-text` (embeddings).

### Arize Phoenix (Optional Tracing)

Phoenix is instrumented via OpenTelemetry at API startup in `app/api/main.py`. If the Phoenix server is not reachable, the exception is caught and the API starts without tracing. No data flows through Phoenix during normal operation — it only receives telemetry spans from LangChain calls.

---

## State Management

### Frontend (Streamlit)

Streamlit uses `st.session_state` for in-memory state within a browser tab:

| Key | Type | Purpose |
|-----|------|---------|
| `session_id` | `str` (UUID4) | Stable identifier for this chat session, generated once per page load |
| `messages` | `list[dict]` | Local copy of the chat history rendered in the UI |

On first load, `messages` is populated by calling `GET /history/{session_id}`, so conversations persist across page refreshes.

### Backend (FastAPI)

The API is stateless — no in-memory session state. All persistence is delegated to:

- **ChromaDB** (`data/chroma_db/`): stores document embeddings, persisted to disk between restarts.
- **SQLite** (`data/chat_history.db`): stores per-session chat messages via `SQLChatMessageHistory`. Created automatically on first use.
