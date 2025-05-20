# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# -------------------------------
# Usuario
# -------------------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

# -------------------------------
# Roles
# -------------------------------

class RoleBase(BaseModel):
    name: str

class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True

# -------------------------------
# Relación Usuario ↔ Rol
# -------------------------------

class UserRoleResponse(BaseModel):
    id: int
    user_id: int
    role_id: int

    class Config:
        orm_mode = True

# -------------------------------
# Imagen / Tarea de imagen
# -------------------------------

class ImageTaskBase(BaseModel):
    image_path: str
    transformation: Optional[dict] = None

class ImageTaskCreate(ImageTaskBase):
    pass

class ImageTaskResponse(ImageTaskBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True

# -------------------------------
# Logs de tareas
# -------------------------------

class TaskLogResponse(BaseModel):
    id: int
    task_id: int
    log_message: str
    created_at: datetime

    class Config:
        orm_mode = True

# -------------------------------
# Auth
# -------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
