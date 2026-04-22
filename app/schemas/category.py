from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import re


class CategoryCreate(BaseModel):
    name: str
    color: Optional[str] = "#6366f1"

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        if v and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Cor deve ser um hex válido, ex: #ff5733")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Nome da categoria deve ter no mínimo 2 caracteres")
        return v.strip()


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}