from pydantic import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    DB_URL: str = 'mysql+asyncmy://root:root@localhost/seed?charset=utf8mb4'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive: True


settings = Settings()