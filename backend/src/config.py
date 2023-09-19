from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "gogame"
    reset_db_tables: bool = True

    # Filled by `.env` file
    db_driver: str = ""
    db_user: str = ""
    db_password: str = ""
    db_host: str = ""
    db_port: str = ""
    db_name: str = ""

    cors_allow_origins: list = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5173",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()