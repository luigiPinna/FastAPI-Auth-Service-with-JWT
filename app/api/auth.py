from datetime import datetime, timedelta, UTC
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.models.token import BlacklistedToken
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenData, TokenResponse, RefreshTokenRequest

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthError(Exception):
    """Eccezione personalizzata per errori di autenticazione"""

    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un access token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(UTC),
        "type": "access"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Crea un refresh token JWT"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(UTC),
        "type": "refresh"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, expected_type: str = "access") -> TokenData:
    """Verifica e decodifica un token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Verifica il tipo di token
        token_type = payload.get("type")
        if token_type != expected_type:
            raise AuthError(f"Invalid token type. Expected {expected_type}, got {token_type}")

        email: str = payload.get("sub")
        if email is None:
            raise AuthError("Token missing subject")

        return TokenData(email=email, token_type=token_type)

    except JWTError as e:
        raise AuthError(f"Token validation failed: {str(e)}")


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    """Ottiene l'utente corrente dal token"""
    try:
        # Verifica se il token è nella blacklist
        blacklisted = db.query(BlacklistedToken).filter(
            BlacklistedToken.token == token
        ).first()
        if blacklisted:
            raise AuthError("Token has been revoked")

        # Verifica il token
        token_data = verify_token(token, "access")

        # Cerca l'utente nel database
        user = db.query(User).filter(User.email == token_data.email).first()
        if user is None:
            raise AuthError("User not found")

        if not user.is_active:
            raise AuthError("User account is disabled")

        return user

    except AuthError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
        user_in: UserCreate,
        db: Session = Depends(get_db)
) -> Any:
    """Registra un nuovo utente"""
    try:
        # Verifica se l'utente esiste già
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Crea nuovo utente
        user = User(
            email=user_in.email,
            name=user_in.name,
            hashed_password=User.get_password_hash(user_in.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Crea tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


@router.post("/login", response_model=Token)
async def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Autenticazione utente"""
    # Cerca l'utente
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verifica credenziali
    if not user or not User.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifica se l'account è attivo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled"
        )

    # Crea tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
        refresh_request: RefreshTokenRequest,
        db: Session = Depends(get_db)
) -> Any:
    """Rinnova l'access token usando il refresh token"""
    try:
        # Verifica il refresh token
        token_data = verify_token(refresh_request.refresh_token, "refresh")

        # Cerca l'utente
        user = db.query(User).filter(User.email == token_data.email).first()
        if not user:
            raise AuthError("User not found")

        if not user.is_active:
            raise AuthError("User account is disabled")

        # Crea nuovo access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    except AuthError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/logout", response_model=TokenResponse)
async def logout(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> Any:
    """Logout utente (blacklist del token)"""
    try:
        # Verifica che il token sia valido prima di metterlo in blacklist
        verify_token(token, "access")

        # Aggiungi il token alla blacklist
        blacklisted_token = BlacklistedToken(token=token)
        db.add(blacklisted_token)
        db.commit()

        return {"message": "Successfully logged out"}

    except AuthError:
        # Anche se il token non è valido, consideriamo il logout riuscito
        return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
        current_user: User = Depends(get_current_user),
) -> Any:
    """Ottiene i dati dell'utente corrente"""
    return current_user


@router.get("/verify-token", response_model=TokenResponse)
async def verify_token_endpoint(
        current_user: User = Depends(get_current_user),
) -> Any:
    """Verifica se il token è ancora valido"""
    return {"message": "Token is valid"}