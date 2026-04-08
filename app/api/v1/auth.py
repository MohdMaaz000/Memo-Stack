from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token, TokenRefresh
from app.services import auth as auth_service

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    return auth_service.authenticate(db, form_data)

@router.post("/refresh", response_model=Token)
def refresh_token(
    *,
    db: Session = Depends(deps.get_db),
    token_in: TokenRefresh,
) -> Any:
    """
    Refresh an access token using a refresh token.
    """
    return auth_service.refresh(db, token_in.refresh_token)

@router.post("/register", response_model=UserSchema)
def register_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    return auth_service.register(db, user_in)
