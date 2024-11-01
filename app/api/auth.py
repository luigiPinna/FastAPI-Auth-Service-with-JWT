from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_tokens, verify_token
from app.core.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if User.get_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user_db = User.create(db, user)
    return create_tokens({"sub": str(user_db.id), "email": user_db.email})


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_db = User.authenticate(db, user.email, user.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return create_tokens({"sub": str(user_db.id), "email": user_db.email})


@router.post("/refresh")
def refresh_token(current_token: str = Depends(verify_token)):
    return create_tokens({"sub": current_token["sub"], "email": current_token["email"]})
