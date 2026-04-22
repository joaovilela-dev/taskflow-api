from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import category_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["🗂️ Categorias"])


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cria uma nova categoria para o usuário autenticado."""
    return category_service.create_category(db, data, current_user)


@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista todas as categorias do usuário autenticado."""
    return category_service.list_categories(db, current_user)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove uma categoria. As tarefas vinculadas ficam sem categoria."""
    return category_service.delete_category(db, category_id, current_user)