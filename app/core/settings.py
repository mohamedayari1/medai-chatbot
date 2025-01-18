from pathlib import Path
from typing import Optional
import os

from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings(BaseSettings):
    EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_MAX_INPUT_LENGTH: int = 256
    EMBEDDING_SIZE: int = 384
    EMBEDDING_MODEL_DEVICE: str = "cpu" 
    
    
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    MONGO_URI: str = "mongodb+srv://zoldyck:zoldyck@cluster0.kjantw5.mongodb.net/"
    DEFAULT_MAX_HISTORY: int = 150
    MODEL_TOKEN_LIMITS: dict = {"gpt-3.5-turbo": 4096, "claude-2": 1e5}
    UPLOAD_FOLDER: str = "inputs"
    VECTOR_STORE: str = "qdrant" #  "faiss" or "elasticsearch" or "qdrant" or "milvus" or "lancedb"
    RETRIEVERS_ENABLED: list = ["classic_rag"] # also brave_search

    # LLM Cache
    CACHE_REDIS_URL: str = "redis://localhost:6379/2"

    API_URL: str = "http://localhost:8000"  # backend url for celery worker

    # API_KEY: Optional[str] = None  # LLM api key
    # EMBEDDINGS_KEY: Optional[str] = None  # api key for embeddings (if using openai, just copy API_KEY)
    # OPENAI_API_BASE: Optional[str] = None  # azure openai api base url
    # OPENAI_API_VERSION: Optional[str] = None  # azure openai api version
    # AZURE_DEPLOYMENT_NAME: Optional[str] = None  # azure deployment name for answering
    # AZURE_EMBEDDINGS_DEPLOYMENT_NAME: Optional[str] = None  # azure deployment name for embeddings
    # OPENAI_BASE_URL: Optional[str] = None # openai base url for open ai compatable models

    # Azure OpenAI config
    AZURE_OPENAI_API_KEY: str = "mcOZ1fI1JChD4P0fyyp84wEb6dJ0iIBWaSfOALNXXWwSfjj5mM7gJQQJ99AKACHYHv6XJ3w3AAAAACOGH5AI"
    AZURE_OPENAI_ENDPOINT: str = "https://alach-m3n4py1o-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    OPENAI_API_VERSION: str = "2024-08-01-preview"


    # # Fetching Qdrant credentials from environment variables set by Kubernetes
    # USE_QDRANT_CLOUD: bool = os.getenv("USE_QDRANT_CLOUD", "false").lower() == "true"  # Convert to bool
    # QDRANT_CLOUD_URL: str = os.getenv("QDRANT_CLOUD_URL", "https://default-qdrant-url:6333")
    # QDRANT_APIKEY: str = os.getenv("QDRANT_APIKEY", "")
    

        
    # USE_QDRANT_CLOUD: bool = True # if True, fill in QDRANT_CLOUD_URL and QDRANT_APIKEY
    # QDRANT_CLOUD_URL: str = "https://9edb3e8c-e16e-4980-82d0-b4a006fe30d6.europe-west3-0.gcp.cloud.qdrant.io:6333"
    # QDRANT_APIKEY: str = "Lsrz-MvukvgEaNn5x1ddPM2mBbNZ9qEmY-JW9s-JnSnBwmvcazC7ig"
    

    # Qdrant in AKS
   
    USE_QDRANT_CLOUD: bool = False # if True, fill in QDRANT_CLOUD_URL and QDRANT_APIKEY
    QDRANT_DATABASE_HOST: str = "72.144.114.98"
    QDRANT_DATABASE_PORT: int = 6333   




path = Path(__file__).parent.parent.absolute()
settings = Settings(_env_file=path.joinpath(".env"), _env_file_encoding="utf-8")


