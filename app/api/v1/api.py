from fastapi import APIRouter

from app.api.v1 import auth, users, books, notes, comments

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(notes.router, prefix="/books", tags=["notes"]) # Notes nested theoretically but route prefix is /books for getting notes
api_router.include_router(comments.router, prefix="/notes", tags=["comments"]) # Comments nested under notes
