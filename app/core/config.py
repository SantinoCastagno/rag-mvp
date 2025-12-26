import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")
    PHOENIX_PROJECT_NAME = os.getenv("PHOENIX_PROJECT_NAME", "gemini-rag-lab")

settings = Config()
