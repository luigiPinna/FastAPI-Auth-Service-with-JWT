from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from passlib.context import CryptContext
from app.models.base import Base

# Configurazione per l'hash delle password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica la password in chiaro contro l'hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera l'hash della password"""
        return pwd_context.hash(password)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"