# Gemini RAG Lab

This project is a modular Retrieval Augmented Generation (RAG) system, showcasing:
- **LLM:** Google Gemini 2.5 Flash-Lite
- **Embeddings:** Google Generative AI Embeddings
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
   Create a `.env` file in the root directory by copying `.env.example` and fill in your `GOOGLE_API_KEY`.
   ```bash
   cp .env.example .env
   # Edit .env with your GOOGLE_API_KEY
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

## Notas de desarrollo

- **Tests:** Los tests unitarios e de integración están fuera del alcance de este POC. El proyecto está pensado como demostración de un sistema RAG funcional, no como código de producción.
- **Tracing:** Phoenix es opcional. Si no está corriendo, la API levanta igualmente con un warning en consola.