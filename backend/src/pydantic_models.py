from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


class ModelName(str, Enum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = Field(default=None)
    model: ModelName = Field(default=ModelName.GEMINI_2_5_FLASH)


class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName


class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_timestamp: datetime


class DeleteFileRequest(BaseModel):
    file_id: str


class MessageHistoryItem(BaseModel):
    session_id: str
    user_query: str
    gpt_response: str
    model: str
    created_at: datetime


class SessionSummary(BaseModel):
    session_id: str
    last_activity: datetime
    message_count: int


class HealthResponse(BaseModel):
    status: str