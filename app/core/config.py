from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DashMachine"
    SECRET_KEY: str = "Xmtjkhfn48jRQlubK0IsSn4ynxP6m9rIS0NMpfjs8so"
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS = 30
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"


settings = Settings()
