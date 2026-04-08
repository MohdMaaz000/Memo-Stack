from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.note import Note as NoteSchema, NoteCreate, NoteUpdate
from app.services import note as note_service

router = APIRouter()

@router.get("/{book_id}/notes", response_model=List[NoteSchema])
def read_book_notes(
    book_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve notes for a specific book.
    """
    return note_service.get_notes(db, book_id, skip, limit, current_user)

@router.post("/{book_id}/notes", response_model=NoteSchema)
def create_book_note(
    *,
    book_id: int,
    db: Session = Depends(deps.get_db),
    note_in: NoteCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new note in a book. Only owner can add notes to their books.
    """
    return note_service.create_note(db, book_id, note_in, current_user)

@router.put("/notes/{id}", response_model=NoteSchema)
def update_note(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    note_in: NoteUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a note.
    """
    return note_service.update_note(db, id, note_in, current_user)

@router.delete("/notes/{id}", response_model=NoteSchema)
def delete_note(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a note.
    """
    return note_service.delete_note(db, id, current_user)

