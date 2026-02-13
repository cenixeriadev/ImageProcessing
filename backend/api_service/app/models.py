"""
Re-export all models from the shared package.
This file exists so that existing imports like `from app.models import User`
continue to work without modification.
"""

from shared.models import User, Role, UserRole, ImageTask, TaskLog  # noqa: F401

__all__ = ["User", "Role", "UserRole", "ImageTask", "TaskLog"]
