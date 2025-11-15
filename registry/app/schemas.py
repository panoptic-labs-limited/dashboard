from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Function schemas
class FunctionBase(BaseModel):
    alias: str = Field(..., description="Unique alias for the function")
    code: str = Field(..., description="Python function code as string")
    description: Optional[str] = None
    memory_limit_mb: int = Field(default=200, ge=1, le=512)
    timeout_seconds: int = Field(default=30, ge=1, le=60)


class FunctionCreate(FunctionBase):
    pass


class FunctionUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    memory_limit_mb: Optional[int] = Field(None, ge=1, le=512)
    timeout_seconds: Optional[int] = Field(None, ge=1, le=60)


class FunctionResponse(FunctionBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Execution schemas
class ExecutionRequest(BaseModel):
    params: Dict[str, Any] = Field(default_factory=dict, description="Function parameters")


class ExecutionResponse(BaseModel):
    id: int
    function_id: int
    status: str
    output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None
    memory_used_mb: Optional[float] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
