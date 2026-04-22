import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token

logger = logging.getLogger("TaskFlow API")


def register_user(db: Session, data: UserCreate) -> TokenResponse:
    logger.info(f"Tentativa de registro: {data.email}")

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    logger.info(f"Usuário registrado com sucesso: {user.email} (id={user.id})")

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


def login_user(db: Session, data: UserLogin) -> TokenResponse:
    logger.info(f"Tentativa de login: {data.email}")

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada",
        )

    token = create_access_token({"sub": str(user.id)})
    logger.info(f"Login bem-sucedido: {user.email}")

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )