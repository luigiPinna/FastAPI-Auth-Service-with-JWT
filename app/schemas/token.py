from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema per la risposta del token"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None  # Secondi di validità


class TokenData(BaseModel):
    """Schema per i dati estratti dal token"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    token_type: Optional[str] = None  # access o refresh


class RefreshTokenRequest(BaseModel):
    """Schema per la richiesta di refresh token"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Schema per risposta generica sui token"""
    message: str


class LogoutResponse(BaseModel):
    """Schema per risposta di logout"""
    message: str