from operator import itemgetter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.core.vector_store import get_vector_store

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set")

    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7
    )

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # LCEL Chain Construction
    chain = (
        RunnableParallel({
            "source_documents": itemgetter("query") | retriever,
            "question": itemgetter("query")
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

    return chain
