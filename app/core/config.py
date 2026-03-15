from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash-lite"
    PHOENIX_PROJECT_NAME: str = "gemini-rag-lab"
    RETRIEVER_K: int = 5
    LLM_TEMPERATURE: float = 0.7
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
