from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services import user_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["🔐 Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Cria uma nova conta e retorna o token JWT."""
    return user_service.register_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Autentica o usuário e retorna o token JWT."""
    return user_service.login_user(db, data)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """Retorna os dados do usuário autenticado."""
    return current_user