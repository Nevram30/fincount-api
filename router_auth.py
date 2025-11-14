"""
Authentication router - handles login, register, logout
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import User
from schemas import UserCreate, UserLogin, LoginResponse, RegisterResponse, UserResponse
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login endpoint - authenticates user and returns JWT token
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    # Return token and user info
    return {
        "token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "createdAt": user.created_at,
            "updatedAt": user.updated_at
        }
    }


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register endpoint - creates new user account
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.id, "email": new_user.email},
        expires_delta=access_token_expires
    )
    
    # Return token and user info
    return {
        "token": access_token,
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "role": new_user.role,
            "createdAt": new_user.created_at,
            "updatedAt": new_user.updated_at
        }
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout endpoint - in JWT, logout is handled client-side
    This endpoint can be used for logging or token blacklisting
    """
    return {"message": "Logged out successfully"}
