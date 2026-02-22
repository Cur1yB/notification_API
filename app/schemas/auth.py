from pydantic import BaseModel


# requests
class RegisterIn(BaseModel):
    username: str
    password: str


class LoginIn(BaseModel):
    username: str
    password: str


class RefreshIn(BaseModel):
    refresh: str


# responses


class TokenPairResponse(BaseModel):
    access: str
    refresh: str


class RegisterResponse(BaseModel):
    user_id: int
    access: str
    refresh: str


class RefreshRequest(BaseModel):
    refresh: str


class AccessTokenResponse(BaseModel):
    access: str
