from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schema base per User"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema per la creazione di un utente"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema per l'aggiornamento di un utente"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """Schema per utente dal database"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}  # Pydantic v2 syntax


class UserResponse(UserBase):
    """Schema per la risposta pubblica dell'utente"""
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}