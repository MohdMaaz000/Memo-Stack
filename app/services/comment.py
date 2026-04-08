from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.note import Note
from app.models.book import Book
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate

def get_comments(db: Session, note_id: int, skip: int, limit: int, current_user: User) -> List[Comment]:
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    book = db.query(Book).filter(Book.id == note.book_id).first()
    if not book.is_public and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return db.query(Comment).filter(Comment.note_id == note_id).offset(skip).limit(limit).all()

def create_comment(db: Session, note_id: int, comment_in: CommentCreate, current_user: User) -> Comment:
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    book = db.query(Book).filter(Book.id == note.book_id).first()
    if not book.is_public and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    comment = Comment(
        content=comment_in.content,
        note_id=note.id,
        user_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def update_comment(db: Session, id: int, comment_in: CommentUpdate, current_user: User) -> Comment:
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
        
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = comment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
        
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, id: int, current_user: User) -> Comment:
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    note = db.query(Note).filter(Note.id == comment.note_id).first()
    book = db.query(Book).filter(Book.id == note.book_id).first()
    
    if comment.user_id != current_user.id and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    db.delete(comment)
    db.commit()
    return comment
