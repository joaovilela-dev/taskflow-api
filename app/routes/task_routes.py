from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, PaginatedTasks
from app.models.task import TaskStatus, TaskPriority
from app.services import task_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["📋 Tarefas"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cria uma nova tarefa para o usuário autenticado."""
    return task_service.create_task(db, data, current_user)


@router.get("/", response_model=PaginatedTasks)
def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filtrar por status"),
    priority: Optional[TaskPriority] = Query(None, description="Filtrar por prioridade"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoria"),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista as tarefas do usuário com filtros e paginação.
    - **status**: pending | in_progress | done
    - **priority**: low | medium | high
    - **category_id**: ID de uma categoria existente
    """
    return task_service.list_tasks(db, current_user, status, priority, category_id, page, per_page)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna os detalhes de uma tarefa específica."""
    return task_service.get_task(db, task_id, current_user)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Atualiza os dados de uma tarefa. Apenas campos enviados serão alterados."""
    return task_service.update_task(db, task_id, data, current_user)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove permanentemente uma tarefa."""
    return task_service.delete_task(db, task_id, current_user)