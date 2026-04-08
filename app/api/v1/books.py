from typing import Any, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.book import Book as BookSchema, BookCreate, BookUpdate
from app.services import book as book_service

router = APIRouter()

@router.get("/", response_model=List[BookSchema])
def read_books(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve books. Returns all public books and the user's private books.
    Supports filtering by search query `q`.
    """
    return book_service.get_books(db, skip, limit, q, current_user)

@router.post("/", response_model=BookSchema)
def create_book(
    *,
    db: Session = Depends(deps.get_db),
    book_in: BookCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new book.
    """
    return book_service.create_book(db, book_in, current_user)

@router.put("/{id}", response_model=BookSchema)
def update_book(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    book_in: BookUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a book. Only owner can update.
    """
    return book_service.update_book(db, id, book_in, current_user)

@router.get("/{id}", response_model=BookSchema)
def read_book(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get book by ID.
    """
    return book_service.get_book(db, id, current_user)

@router.delete("/{id}", response_model=BookSchema)
def delete_book(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a book. Only owner can delete.
    """
    return book_service.delete_book(db, id, current_user)

