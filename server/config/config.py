from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str
  POSTGRES_HOST: str = "localhost"
  POSTGRES_PORT: str = "65432"
  
  OPENAI_API_KEY: str

  def get_database_uri(self) -> str:
    return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
  
  class Config:
    env_file = ".env"
    case_sensitive = True

settings = Settings()

__all__ = ["settings"]

