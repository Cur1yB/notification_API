from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TTL_SECONDS: int = 15 * 60 # min * sec
    REFRESH_TTL_SECONDS: int = 7 * 24 * 60 * 60 # days * hours * min * sec
    DEFAULT_AVATAR_URL: str = "#" # WASH ME


settings = Settings()