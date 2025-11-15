"""
Sessions router - handles CRUD operations for counting sessions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Session as SessionModel
from schemas import SessionCreate, SessionUpdate, SessionResponse, SessionListResponse, SessionCreateResponse
from auth import get_current_user

router = APIRouter()


def session_to_dict(session: SessionModel) -> dict:
    """Convert SQLAlchemy session model to dictionary matching Flutter format"""
    return {
        "id": session.id,
        "batchId": session.batch_id,
        "species": session.species,
        "location": session.location,
        "notes": session.notes,
        "counts": session.counts,
        "timestamp": session.timestamp,
        "imageUrl": session.image_url or ""
    }


@router.get("", response_model=SessionListResponse)
async def get_sessions(
    db: Session = Depends(get_db)
):
    """
    Get all sessions (No authentication required)
    """
    sessions = db.query(SessionModel).all()
    
    sessions_list = [session_to_dict(s) for s in sessions]
    
    return {
        "success": True,
        "data": {
            "sessions": sessions_list,
            "pagination": {
                "total": len(sessions_list),
                "page": 1,
                "limit": 100
            }
        }
    }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SessionCreateResponse)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new counting session (No authentication required)
    Auto-creates batch if it doesn't exist
    """
    from models import Batch
    
    # Check if batch exists, if not create it
    batch = db.query(Batch).filter(Batch.id == session_data.batchId).first()
    if not batch:
        # Create batch with the ID from Flutter
        batch = Batch(
            id=session_data.batchId,
            name=f"Auto-created batch {session_data.batchId[:8]}",
            description="Automatically created from session",
            user_id="fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
            is_active=True
        )
        db.add(batch)
        db.commit()
    
    new_session = SessionModel(
        batch_id=session_data.batchId,
        user_id="fa1c3896-50a9-41b8-a573-a4c9dc1266bf",  # Admin user ID
        species=session_data.species,
        location=session_data.location,
        notes=session_data.notes,
        counts=session_data.counts,
        timestamp=session_data.timestamp,
        image_url=session_data.imageUrl
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "success": True,
        "data": session_to_dict(new_session),
        "message": "Session created successfully"
    }


@router.get("/batch/{batch_id}", response_model=List[SessionResponse])
async def get_batch_sessions(
    batch_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all sessions for a specific batch
    """
    sessions = db.query(SessionModel).filter(
        SessionModel.batch_id == batch_id,
        SessionModel.user_id == current_user["sub"]
    ).all()
    
    return [session_to_dict(s) for s in sessions]


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    session_data: SessionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing session
    """
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user["sub"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Update fields if provided
    if session_data.species is not None:
        session.species = session_data.species
    if session_data.location is not None:
        session.location = session_data.location
    if session_data.notes is not None:
        session.notes = session_data.notes
    if session_data.counts is not None:
        session.counts = session_data.counts
    
    db.commit()
    db.refresh(session)
    
    return session_to_dict(session)


@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a session
    """
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user["sub"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    db.delete(session)
    db.commit()
    
    return {"message": "Session deleted successfully"}
