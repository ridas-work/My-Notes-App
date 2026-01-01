from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.post("/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # NEW - requires authentication
):
    """Create a new note (requires authentication)"""
    return crud.create_note(db=db, note=note, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Note])
def get_notes(
    skip: int = 0, 
    limit: int = 100, 
    tag: Optional[str] = None, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # NEW - requires authentication
):
    """Get all notes for current user (requires authentication)"""
    return crud.get_notes(db=db, user_id=current_user.id, skip=skip, limit=limit, tag=tag)

@router.get("/{note_id}", response_model=schemas.Note)
def get_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # NEW - requires authentication
):
    """Get a specific note (requires authentication)"""
    db_note = crud.get_note(db=db, note_id=note_id, user_id=current_user.id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=schemas.Note)
def update_note(
    note_id: int, 
    note: schemas.NoteUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # NEW - requires authentication
):
    """Update a note (requires authentication)"""
    db_note = crud.update_note(db=db, note_id=note_id, note_update=note, user_id=current_user.id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.delete("/{note_id}")
def delete_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # NEW - requires authentication
):
    """Delete a note (requires authentication)"""
    success = crud.delete_note(db=db, note_id=note_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

@router.get("/search/", response_model=List[schemas.Note])
def search_notes(
    q: str,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Search notes by keyword in title or content (requires authentication)"""
    if not q or q.strip() == "":
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    return crud.search_notes(db=db, user_id=current_user.id, query=q, skip=skip, limit=limit)