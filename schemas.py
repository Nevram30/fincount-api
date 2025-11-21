"""
Pydantic schemas for request/response validation
These match the Flutter app's data models
"""
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, Dict
from enum import Enum


# ============= Enums for Validation =============

class SpeciesEnum(str, Enum):
    """Valid fish species"""
    TILAPIA = "Tilapia"
    BANGUS = "Bangus (Milkfish)"

class LocationEnum(str, Enum):
    """Valid pond locations"""
    CAGANGOHAN = "Cagangohan"
    SOUTHERN = "Southern"

# ============= User Schemas =============

class UserBase(BaseModel):
    full_name: str
    username: str
    user_type: str  # "Admin" or "Staff"

class UserCreate(UserBase):
    password: str
    confirm_password: str
    
    def validate_passwords(self):
        """Validate that passwords match"""
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    user_type: Optional[str] = None

class UserResponse(UserBase):
    id: str
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
    # Allow extra fields from Flutter app but ignore them
    class Config:
        extra = "ignore"

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
    species: SpeciesEnum  # Validated against enum
    location: LocationEnum  # Validated against enum
    notes: str
    counts: Dict[str, int]  # e.g., {"Fish": 100}
    timestamp: str
    imageUrl: str
    userId: Optional[str] = None  # Optional user ID, will use default admin if not provided
    
    @validator('species', pre=True)
    def validate_species(cls, v):
        """Validate species against allowed values"""
        if isinstance(v, str):
            # Try to match the string to enum
            try:
                return SpeciesEnum(v)
            except ValueError:
                valid_values = [e.value for e in SpeciesEnum]
                raise ValueError(f"Invalid species '{v}'. Must be one of: {', '.join(valid_values)}")
        return v
    
    @validator('location', pre=True)
    def validate_location(cls, v):
        """Validate location against allowed values"""
        if isinstance(v, str):
            # Try to match the string to enum
            try:
                return LocationEnum(v)
            except ValueError:
                valid_values = [e.value for e in LocationEnum]
                raise ValueError(f"Invalid location '{v}'. Must be one of: {', '.join(valid_values)}")
        return v

class SessionCreate(SessionBase):
    # Allow extra fields from Flutter app but ignore them
    class Config:
        extra = "ignore"

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
