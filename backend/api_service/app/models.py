from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(300), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")
    last_login = Column(TIMESTAMP)

    roles = relationship("UserRole", back_populates="user", cascade="all, delete")
    tasks = relationship("ImageTask", back_populates="user", cascade="all, delete")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user_roles")


class ImageTask(Base):
    __tablename__ = "image_tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")
    completed_at = Column(TIMESTAMP)
    transformation = Column(JSONB)

    user = relationship("User", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete")


class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("image_tasks.id", ondelete="CASCADE"), nullable=False)
    log_message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")

    task = relationship("ImageTask", back_populates="logs")
