from pydantic import BaseModel, Field


# requests
class RegisterIn(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=72)


class LoginIn(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=72)


class RefreshIn(BaseModel):
    refresh: str


class RefreshRequest(BaseModel):
    refresh: str


# responses
class TokenPairResponse(BaseModel):
    access: str
    refresh: str


class RegisterResponse(BaseModel):
    user_id: int
    access: str
    refresh: str


class AccessTokenResponse(BaseModel):
    access: str
