import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base is imported from shared so all services use the same metadata registry
from shared.database import Base  # noqa: F401 — re-exported for backward compat

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/image_service")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)