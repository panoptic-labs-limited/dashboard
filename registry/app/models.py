from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    functions = relationship("Function", back_populates="owner")


class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True, index=True, nullable=False)
    code = Column(Text, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Resource configuration
    memory_limit_mb = Column(Integer, default=200)
    timeout_seconds = Column(Integer, default=30)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="functions")
    executions = relationship("Execution", back_populates="function")


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    function_id = Column(Integer, ForeignKey("functions.id"), nullable=False)

    # Execution details
    input_params = Column(JSON)
    output = Column(JSON)
    status = Column(String, nullable=False)  # success, error, timeout
    error_message = Column(Text)

    # Metrics
    execution_time_ms = Column(Float)
    memory_used_mb = Column(Float)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    function = relationship("Function", back_populates="executions")
