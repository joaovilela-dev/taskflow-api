import logging
from typing import Optional
from math import ceil
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.category import Category
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, PaginatedTasks

logger = logging.getLogger("TaskFlow API")


def create_task(db: Session, data: TaskCreate, current_user: User) -> Task:
    if data.category_id:
        cat = db.query(Category).filter(
            Category.id == data.category_id,
            Category.owner_id == current_user.id,
        ).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

    task = Task(**data.model_dump(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"Tarefa criada: '{task.title}' por user_id={current_user.id}")
    return task


def list_tasks(
    db: Session,
    current_user: User,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    category_id: Optional[int] = None,
    page: int = 1,
    per_page: int = 10,
) -> PaginatedTasks:
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if category_id:
        query = query.filter(Task.category_id == category_id)

    total = query.count()
    items = query.order_by(Task.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedTasks(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=ceil(total / per_page) if total > 0 else 1,
        items=items,
    )


def get_task(db: Session, task_id: int, current_user: User) -> Task:
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate, current_user: User) -> Task:
    task = get_task(db, task_id, current_user)

    if data.category_id is not None:
        cat = db.query(Category).filter(
            Category.id == data.category_id,
            Category.owner_id == current_user.id,
        ).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    logger.info(f"Tarefa atualizada: id={task_id} por user_id={current_user.id}")
    return task


def delete_task(db: Session, task_id: int, current_user: User) -> dict:
    task = get_task(db, task_id, current_user)
    db.delete(task)
    db.commit()
    logger.info(f"Tarefa deletada: id={task_id} por user_id={current_user.id}")
    return {"message": "Tarefa removida com sucesso"}