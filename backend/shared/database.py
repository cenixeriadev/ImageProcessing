"""
Shared database base — single source of truth for the declarative Base.
Both api_service and worker_service import Base from here so that all
ORM models share the same metadata registry.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
