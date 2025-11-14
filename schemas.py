"""
Pydantic schemas for request/response validation
These match the Flutter app's data models
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict

# ============= User Schemas =============

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class UserResponse(UserBase):
    id: str
    role: Optional[str] = "user"
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============= Batch Schemas =============

class BatchBase(BaseModel):
    name: str
    description: Optional[str] = None
    isActive: bool = True

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    isActive: Optional[bool] = None

class BatchResponse(BatchBase):
    id: str
    userId: str
    totalCount: int = 0
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============= Session Schemas =============

class SessionBase(BaseModel):
    batchId: str
    species: str
    location: str
    notes: str
    counts: Dict[str, int]  # e.g., {"alive": 100, "dead": 5}
    timestamp: str
    imageUrl: str

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    species: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    counts: Optional[Dict[str, int]] = None

class SessionResponse(SessionBase):
    id: str

    class Config:
        from_attributes = True


# ============= Auth Response Schemas =============

class LoginResponse(BaseModel):
    token: str
    user: UserResponse

class RegisterResponse(BaseModel):
    token: str
    user: UserResponse


# ============= API Response Wrappers =============

class BatchListResponse(BaseModel):
    success: bool = True
    data: Dict

class SessionListResponse(BaseModel):
    success: bool = True
    data: Dict

class SessionCreateResponse(BaseModel):
    success: bool = True
    data: SessionResponse
    message: str
