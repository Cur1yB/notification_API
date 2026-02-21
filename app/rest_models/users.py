# app/rest_models/users.py
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


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