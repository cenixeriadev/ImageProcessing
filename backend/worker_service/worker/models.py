from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class ImageTask(Base):
    __tablename__ = "image_tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    image_path = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP)
    transformation = Column(JSONB)

    logs = relationship("TaskLog", back_populates="task", cascade="all, delete")


class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("image_tasks.id", ondelete="CASCADE"), nullable=False)
    log_message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    task = relationship("ImageTask", back_populates="logs")
