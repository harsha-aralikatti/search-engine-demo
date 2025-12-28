from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # -----------------------
    # POSTGRES
    # -----------------------
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # -----------------------
    # REDIS
    # -----------------------
    REDIS_HOST: str
    REDIS_PORT: int

    # -----------------------
    # QDRANT
    # -----------------------
    QDRANT_HOST: str
    QDRANT_PORT: int

    # -----------------------
    # LOCAL EMBEDDINGS
    # -----------------------
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384

    class Config:
        env_file = ".env"


settings = Settings()
