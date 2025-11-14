"""
SQLAlchemy database models
These define the database tables structure
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


def generate_uuid():
    """Generate a unique ID"""
    return str(uuid.uuid4())


class User(Base):
    """User model - stores user account information"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    batches = relationship("Batch", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Batch(Base):
    """Batch model - stores batch information"""
    __tablename__ = "batches"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    total_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="batches")
    sessions = relationship("Session", back_populates="batch", cascade="all, delete-orphan")


class Session(Base):
    """Session model - stores counting session data"""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    batch_id = Column(String, ForeignKey("batches.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    species = Column(String, nullable=False)
    location = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    counts = Column(JSON, nullable=False)  # Stores {"alive": 100, "dead": 5}
    timestamp = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="sessions")
    batch = relationship("Batch", back_populates="sessions")
