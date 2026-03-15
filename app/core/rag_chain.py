from operator import itemgetter
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.core.config import settings
from app.core.vector_store import get_vector_store

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_session_history(session_id: str):
    os.makedirs("data", exist_ok=True)
    return SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///data/chat_history.db")

def get_rag_chain():
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set")

    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.LLM_TEMPERATURE
    )

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": settings.RETRIEVER_K})

    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}
    
    Chat History:
    {chat_history}

    Question: {question}
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question", "chat_history"]
    )

    # LCEL Chain Construction
    chain = (
        RunnableParallel({
            "source_documents": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history")
        })
        .assign(result=(
            RunnablePassthrough.assign(
                context=lambda x: format_docs(x["source_documents"])
            )
            | PROMPT
            | llm
            | StrOutputParser()
        ))
    )

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="result"
    )

    return chain_with_history
