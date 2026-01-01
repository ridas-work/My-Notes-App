from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@router.get("/", response_model=List[schemas.Tag])
def get_all_tags(db: Session = Depends(get_db)):
    """Get all available tags"""
    return crud.get_all_tags(db=db)