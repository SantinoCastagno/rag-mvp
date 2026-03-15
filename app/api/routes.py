from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from app.core.ingestion import process_file
from app.core.rag_chain import get_rag_chain, get_session_history

router = APIRouter()

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., min_length=1, max_length=100)

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

class Message(BaseModel):
    role: str
    content: str

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".md")):
        raise HTTPException(status_code=400, detail="Only PDF and Markdown files are supported")
    
    try:
        content = await file.read()
        num_chunks = process_file(content, file.filename)
        return {"message": f"Successfully ingested {file.filename}", "chunks": num_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=List[Message])
async def get_history(session_id: str):
    try:
        history = get_session_history(session_id)
        messages = []
        for msg in history.messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            messages.append(Message(role=role, content=msg.content))
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        chain = get_rag_chain()
        result = chain.invoke(
            {"question": request.question},
            config={"configurable": {"session_id": request.session_id}}
        )
        
        answer = result.get("result", "")
        source_docs = result.get("source_documents", [])
        sources = [doc.metadata.get("source", "unknown") for doc in source_docs]
        
        # Deduplicate sources
        sources = list(set(sources))
        
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))