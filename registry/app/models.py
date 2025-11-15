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
    components = relationship("Component", back_populates="owner")
    dashboards = relationship("Dashboard", back_populates="owner")


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


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True, index=True, nullable=False)
    class_name = Column(String, nullable=False)
    source_code = Column(Text, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Component metadata stored as JSON
    parameters = Column(JSON, default=list)  # List of parameter definitions
    metadata = Column(JSON, default=dict)  # Additional metadata

    # Resource configuration
    memory_limit_mb = Column(Integer, default=200)
    timeout_seconds = Column(Integer, default=30)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="components")
    component_executions = relationship("ComponentExecution", back_populates="component")


class ComponentExecution(Base):
    __tablename__ = "component_executions"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id"), nullable=False)

    # Execution details
    stage = Column(String, nullable=False)  # load, load_transform, load_transform_render
    input_params = Column(JSON)
    output = Column(JSON)
    status = Column(String, nullable=False)  # success, error, timeout
    error_message = Column(Text)

    # Metrics
    execution_time_ms = Column(Float)
    memory_used_mb = Column(Float)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    component = relationship("Component", back_populates="component_executions")


class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Dashboard structure stored as JSON
    structure = Column(JSON, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="dashboards")
