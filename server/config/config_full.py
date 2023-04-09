from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str
  POSTGRES_HOST: str = "localhost"  # Default value
  POSTGRES_PORT: str = "65432"  # Default value
  
  OPENAI_API_KEY: str
  TAVILY_API_KEY: str
  SERPAPI_API_KEY: str
  
  # MinIO S3 Storage
  MINIO_ENDPOINT: str = "minio:9000"
  MINIO_ACCESS_KEY: str = "user"
  MINIO_SECRET_KEY: str = "password"
  MINIO_BUCKET: str = "media"
  MINIO_SECURE: bool = False

  def get_database_uri(self) -> str:
    return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
  
  class Config:
    env_file = ".env"
    case_sensitive = True
    extra = "allow"

settings = Settings()

def validate_settings():
    required_fields = [
        'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', 'POSTGRES_HOST', 'POSTGRES_PORT',
        'OPENAI_API_KEY', 'TAVILY_API_KEY', 'SERPAPI_API_KEY'
    ]
    missing = [field for field in required_fields if not getattr(settings, field)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

__all__ = ["settings", "validate_settings"]

