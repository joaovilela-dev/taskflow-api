import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate

logger = logging.getLogger("TaskFlow API")


def create_category(db: Session, data: CategoryCreate, current_user: User) -> Category:
    existing = db.query(Category).filter(
        Category.name == data.name,
        Category.owner_id == current_user.id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já possui uma categoria com esse nome",
        )

    category = Category(**data.model_dump(), owner_id=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    logger.info(f"Categoria criada: '{category.name}' por user_id={current_user.id}")
    return category


def list_categories(db: Session, current_user: User) -> list[Category]:
    return db.query(Category).filter(Category.owner_id == current_user.id).all()


def delete_category(db: Session, category_id: int, current_user: User) -> dict:
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.owner_id == current_user.id,
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(category)
    db.commit()
    logger.info(f"Categoria deletada: id={category_id} por user_id={current_user.id}")
    return {"message": "Categoria removida com sucesso"}