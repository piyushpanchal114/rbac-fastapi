from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project Settings"""
    db_url: str
    echo_sql: bool = True
    debug: bool = True
    project_name: str = "FastAPI RBAC"
    secret: str
    algorithm: str
    access_token_expire: int = 15
    refresh_token_expire: int = 30

    class Config:
        env_file = "../.env"


settings = Settings()
