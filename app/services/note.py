from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.note import Note
from app.models.book import Book
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate

def get_notes(db: Session, book_id: int, skip: int, limit: int, current_user: User) -> List[Note]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_public and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return db.query(Note).filter(Note.book_id == book_id).offset(skip).limit(limit).all()

def create_note(db: Session, book_id: int, note_in: NoteCreate, current_user: User) -> Note:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    note = Note(
        title=note_in.title,
        content=note_in.content,
        book_id=book.id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def update_note(db: Session, id: int, note_in: NoteUpdate, current_user: User) -> Note:
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    book = db.query(Book).filter(Book.id == note.book_id).first()
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = note_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
        
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, id: int, current_user: User) -> Note:
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    book = db.query(Book).filter(Book.id == note.book_id).first()
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    db.delete(note)
    db.commit()
    return note
