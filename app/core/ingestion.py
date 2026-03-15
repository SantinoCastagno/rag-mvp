import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.vector_store import add_documents_to_store
from app.core.config import settings
import tempfile

def process_file(file_content: bytes, filename: str):
    file_extension = os.path.splitext(filename)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(file_content)
        tmp_file_path = tmp_file.name

    try:
        if file_extension == ".pdf":
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()
        elif file_extension == ".md":
            loader = TextLoader(tmp_file_path) 
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        
        chunks = text_splitter.split_documents(documents)
        add_documents_to_store(chunks)
        
        return len(chunks)

    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
