from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Code Search API"
    API_V1_STR: str = "/api/v1"
    
    # Model settings
    MODEL_NAME: str = "Salesforce/codet5p-220m"  # Base CodeT5+ model
    MODEL_EMBEDDING_SIZE: int = 768
    MAX_SEQUENCE_LENGTH: int = 512
    DEVICE: str = "cuda"  # or "cpu" based on availability
    
    # Search settings
    FAISS_INDEX_PATH: Path = Path("indexes/codesearch.faiss")
    TOP_K_RESULTS: int = 5
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Database settings
    VECTOR_DB_TYPE: str = "faiss"  # or "milvus"
    
    class Config:
        env_file = ".env"

settings = Settings() 