from dataclasses import dataclass


@dataclass
class DummySettings:
    JWT_SECRET: str = "SECRET"
    JWT_ALG: str = "HS256"
    ACCESS_TTL_SECONDS: int = 900
    REFRESH_TTL_SECONDS: int = 86400
    DEFAULT_AVATAR_URL: str = "https://example.com/default.png"


@dataclass
class DummyUser:
    id: int
    username: str
    password_hash: str = "HASHED"
    avatar_url: str = DummySettings.DEFAULT_AVATAR_URL