from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.comment import Comment as CommentSchema, CommentCreate, CommentUpdate
from app.services import comment as comment_service

router = APIRouter()

@router.get("/{note_id}/comments", response_model=List[CommentSchema])
def read_note_comments(
    note_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve comments for a specific note.
    """
    return comment_service.get_comments(db, note_id, skip, limit, current_user)

@router.post("/{note_id}/comments", response_model=CommentSchema)
def create_note_comment(
    *,
    note_id: int,
    db: Session = Depends(deps.get_db),
    comment_in: CommentCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new comment on a note.
    """
    return comment_service.create_comment(db, note_id, comment_in, current_user)

@router.put("/comments/{id}", response_model=CommentSchema)
def update_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a comment. Only the comment owner can update it.
    """
    return comment_service.update_comment(db, id, comment_in, current_user)

@router.delete("/comments/{id}", response_model=CommentSchema)
def delete_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a comment. Only the comment owner or the book owner can delete it.
    """
    return comment_service.delete_comment(db, id, current_user)

