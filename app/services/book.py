from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate

def get_books(db: Session, skip: int, limit: int, q: Optional[str], current_user: User) -> List[Book]:
    query = db.query(Book).filter(
        or_(Book.owner_id == current_user.id, Book.is_public == True)
    )
    if q:
        query = query.filter(Book.title.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()

def create_book(db: Session, book_in: BookCreate, current_user: User) -> Book:
    book = Book(
        title=book_in.title,
        description=book_in.description,
        cover_image=book_in.cover_image,
        is_public=book_in.is_public,
        owner_id=current_user.id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, id: int, current_user: User) -> Book:
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_public and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return book

def update_book(db: Session, id: int, book_in: BookUpdate, current_user: User) -> Book:
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = book_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
        
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, id: int, current_user: User) -> Book:
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(book)
    db.commit()
    return book
