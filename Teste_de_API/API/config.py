from typing import List

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ANS Healthcare Operators API"
    API_V1_STR: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Files
    DATA_DIR = "data"
    OPERADORAS_CSV = DATA_DIR + "/Relatorio_cadop.csv"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
