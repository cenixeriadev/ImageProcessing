from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String(300) , unique = True , nullable = False)
    created_at = Column(TIMESTAMP, server_default="now()")
    last_login = Column(TIMESTAMP)

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    original_url = Column(Text, nullable=False)
    transformed_url = Column(Text)
    transformation = Column(JSONB)
    image_metadata = Column('metadata', JSONB)  # Changed here
    created_at = Column(TIMESTAMP, server_default="now()")