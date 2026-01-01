from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# ========== USER SCHEMAS (NEW) ==========

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ========== TAG SCHEMAS (UNCHANGED) ==========

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    
    class Config:
        from_attributes = True

# ========== NOTE SCHEMAS (UNCHANGED) ==========

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    tag_names: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Note",
                "content": "This is my first note content",
                "tag_names": ["work", "important"]
            }
        }

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_names: Optional[List[str]] = None

class Note(NoteBase):
    id: int
    user_id: int  # NEW
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []
    
    class Config:
        from_attributes = True