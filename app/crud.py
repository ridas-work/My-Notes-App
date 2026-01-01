from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password

# ============ USER OPERATIONS (NEW) ============

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user"""
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

# ============ TAG OPERATIONS (UNCHANGED) ============

def get_tag_by_name(db: Session, tag_name: str):
    """Get a tag by its name"""
    return db.query(models.Tag).filter(models.Tag.name == tag_name).first()

def get_or_create_tag(db: Session, tag_name: str):
    """Get existing tag or create new one"""
    tag = get_tag_by_name(db, tag_name)
    if not tag:
        tag = models.Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag

def get_all_tags(db: Session):
    """Get all tags"""
    return db.query(models.Tag).all()

# ============ NOTE OPERATIONS (UPDATED - added user_id) ============

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    """Create a new note with tags for a specific user"""
    db_note = models.Note(
        title=note.title,
        content=note.content,
        user_id=user_id  # NEW
    )
    
    # Add tags
    for tag_name in note.tag_names:
        tag = get_or_create_tag(db, tag_name)
        db_note.tags.append(tag)
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_note(db: Session, note_id: int, user_id: int):
    """Get a single note by ID for a specific user"""
    return db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == user_id  # NEW - only user's notes
    ).first()

def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100, tag: str = None):
    """Get all notes for a specific user, optionally filter by tag"""
    query = db.query(models.Note).filter(models.Note.user_id == user_id)  # NEW
    
    # Filter by tag if provided
    if tag:
        query = query.join(models.Note.tags).filter(models.Tag.name == tag)
    
    return query.offset(skip).limit(limit).all()

def update_note(db: Session, note_id: int, note_update: schemas.NoteUpdate, user_id: int):
    """Update a note for a specific user"""
    db_note = get_note(db, note_id, user_id)  # NEW - check ownership
    
    if not db_note:
        return None
    
    # Update title and content if provided
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.content is not None:
        db_note.content = note_update.content
    
    # Update tags if provided
    if note_update.tag_names is not None:
        db_note.tags.clear()
        for tag_name in note_update.tag_names:
            tag = get_or_create_tag(db, tag_name)
            db_note.tags.append(tag)
    
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    """Delete a note for a specific user"""
    db_note = get_note(db, note_id, user_id)  # NEW - check ownership
    
    if not db_note:
        return False
    
    db.delete(db_note)
    db.commit()
    return True

def search_notes(db: Session, user_id: int, query: str, skip: int = 0, limit: int = 100):
    """Search notes by keyword in title or content"""
    search_pattern = f"%{query}%"
    
    return db.query(models.Note).filter(
        models.Note.user_id == user_id,
        (models.Note.title.ilike(search_pattern) | models.Note.content.ilike(search_pattern))
    ).offset(skip).limit(limit).all()