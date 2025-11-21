"""
Sessions router - handles CRUD operations for counting sessions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
import traceback

from database import get_db
from models import Session as SessionModel
from schemas import SessionCreate, SessionUpdate, SessionResponse, SessionListResponse, SessionCreateResponse
from auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    Validates that user exists before creating session/batch
    """
    try:
        logger.info(f"=== Session Creation Request ===")
        logger.info(f"Batch ID: {session_data.batchId}")
        logger.info(f"Species: {session_data.species}")
        logger.info(f"Location: {session_data.location}")
        logger.info(f"Counts: {session_data.counts}")
        logger.info(f"Timestamp: {session_data.timestamp}")
        
        from models import Batch, User
        
        # Get user_id from request or use default admin user
        user_id = session_data.userId
        if not user_id:
            # Use the first admin user as default
            default_user = db.query(User).filter(User.user_type == "Admin").first()
            if not default_user:
                # Fallback to any user
                default_user = db.query(User).first()
            if not default_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="No users found in database. Please create a user first."
                )
            user_id = default_user.id
            logger.info(f"No userId provided, using default admin: {user_id}")
        else:
            logger.info(f"Using provided userId: {user_id}")
        
        # Validate that user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id '{user_id}' not found. Please ensure the user exists in the database."
            )
        
        logger.info(f"✓ User validated: {user.username} ({user.user_type})")
        
        # Check if batch exists, if not create it
        batch = db.query(Batch).filter(Batch.id == session_data.batchId).first()
        if not batch:
            logger.info(f"Creating new batch: {session_data.batchId}")
            # Create batch with validated user_id
            batch = Batch(
                id=session_data.batchId,
                name=f"Auto-created batch {session_data.batchId[:8]}",
                description="Automatically created from session",
                user_id=user_id,  # Use validated user_id
                is_active=True
            )
            db.add(batch)
            db.commit()
            logger.info(f"✓ Batch created successfully with user_id: {user_id}")
        else:
            logger.info(f"✓ Using existing batch: {batch.id}")
        
        logger.info("Creating session...")
        new_session = SessionModel(
            batch_id=session_data.batchId,
            user_id=user_id,  # Use validated user_id
            species=session_data.species.value,  # Get enum value
            location=session_data.location.value,  # Get enum value
            notes=session_data.notes,
            counts=session_data.counts,
            timestamp=session_data.timestamp,
            image_url=session_data.imageUrl
        )
        
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        
        logger.info(f"✓ Session created successfully: {new_session.id}")
        logger.info(f"  User ID: {new_session.user_id}")
        logger.info(f"  Species: {new_session.species}")
        logger.info(f"  Location: {new_session.location}")
        
        return {
            "success": True,
            "data": session_to_dict(new_session),
            "message": "Session created successfully"
        }
        
    except ValueError as e:
        logger.error(f"❌ Validation Error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"❌ Session Creation Error: {str(e)}")
        logger.error(f"Error Type: {type(e).__name__}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


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
