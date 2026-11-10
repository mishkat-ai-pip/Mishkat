from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Content(Base):
    __tablename__ = "contents"
    content_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_ar = Column(Text, nullable=False)
    title_en = Column(Text, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    content_type = Column(String, nullable=False)
    external_url = Column(Text, nullable=False)
    status = Column(String, default="pending")
  
