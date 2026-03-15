# RAG Lab

> [Versión en español](README.es.md)

This project is a modular Retrieval Augmented Generation (RAG) system, showcasing:
- **LLM / Embeddings:** Provider-agnostic via factory pattern — supports **Google Gemini** (default) and **Ollama**. Switch with `LLM_PROVIDER` env variable.
- **Vector Store:** ChromaDB (local persistence)
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Tracing/Eval:** Arize Phoenix
- **Key Feature:** Persistent chat history across sessions using SQLite.

## Setup

1. **Install Dependencies:**
   ```bash
   poetry install
   ```

2. **Environment Variables:**
   Create a `.env` file copying `.env.example` and configure the provider. `GOOGLE_API_KEY` is required only when `LLM_PROVIDER=gemini`.
   ```bash
   cp .env.example .env
   # Edit .env: set LLM_PROVIDER and the corresponding credentials/URLs
   ```

## Running the Application

This project uses a `Makefile` to simplify running the different services. You need to start the Phoenix server, the FastAPI backend, and the Streamlit frontend.

### 1. Start Arize Phoenix (Optional but recommended for tracing)
```bash
make phoenix
```
*Access Phoenix UI at http://localhost:6006*

### 2. Start Backend (FastAPI)
```bash
make api
```
*API docs at http://localhost:8000/docs*

### 3. Start Frontend (Streamlit)
```bash
make ui
```
*Access Chatbot at http://localhost:8501*

## Usage

1. Open the Streamlit app in your browser (after running `make ui`).
2. Upload a PDF or Markdown file via the sidebar.
3. Click "Ingest File".
4. Ask questions in the chat interface. Your conversation history will be persisted for your session.

## Documentation

Detailed technical documentation is available in the [`docs/`](docs/) directory:

- [Architecture](docs/ARCHITECTURE.md)
- [System Flows](docs/SYSTEM_FLOWS.md)
- [Data Models](docs/DATA_MODELS.md)
- [API Protocol](docs/PROTOCOL_API.md)

## Development Notes

- **Tests:** Unit and integration tests are out of scope for this POC. The project is intended as a demonstration of a functional RAG system, not production-ready code.
- **Tracing:** Phoenix is optional. If it is not running, the API will still start with a warning in the console.