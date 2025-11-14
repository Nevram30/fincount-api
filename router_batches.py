"""
Batches router - handles CRUD operations for batches
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Batch
from schemas import BatchCreate, BatchUpdate, BatchResponse, BatchListResponse
from auth import get_current_user

router = APIRouter()


def batch_to_dict(batch: Batch) -> dict:
    """Convert SQLAlchemy batch model to dictionary matching Flutter format"""
    return {
        "id": batch.id,
        "name": batch.name,
        "description": batch.description,
        "userId": batch.user_id,
        "totalCount": batch.total_count,
        "createdAt": batch.created_at.isoformat(),
        "updatedAt": batch.updated_at.isoformat() if batch.updated_at else None,
        "isActive": batch.is_active
    }


@router.get("", response_model=BatchListResponse)
async def get_batches(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all batches for the current user
    """
    batches = db.query(Batch).filter(
        Batch.user_id == current_user["sub"]
    ).all()
    
    batches_list = [batch_to_dict(b) for b in batches]
    
    return {
        "success": True,
        "data": {
            "batches": batches_list
        }
    }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BatchResponse)
async def create_batch(
    batch_data: BatchCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new batch
    """
    new_batch = Batch(
        name=batch_data.name,
        description=batch_data.description,
        user_id=current_user["sub"],
        is_active=batch_data.isActive
    )
    
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    
    return batch_to_dict(new_batch)


@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(
    batch_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific batch by ID
    """
    batch = db.query(Batch).filter(
        Batch.id == batch_id,
        Batch.user_id == current_user["sub"]
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    return batch_to_dict(batch)


@router.put("/{batch_id}", response_model=BatchResponse)
async def update_batch(
    batch_id: str,
    batch_data: BatchUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing batch
    """
    batch = db.query(Batch).filter(
        Batch.id == batch_id,
        Batch.user_id == current_user["sub"]
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    # Update fields if provided
    if batch_data.name is not None:
        batch.name = batch_data.name
    if batch_data.description is not None:
        batch.description = batch_data.description
    if batch_data.isActive is not None:
        batch.is_active = batch_data.isActive
    
    db.commit()
    db.refresh(batch)
    
    return batch_to_dict(batch)


@router.delete("/{batch_id}")
async def delete_batch(
    batch_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a batch
    """
    batch = db.query(Batch).filter(
        Batch.id == batch_id,
        Batch.user_id == current_user["sub"]
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    db.delete(batch)
    db.commit()
    
    return {"message": "Batch deleted successfully"}
