from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteInDBBase(NoteBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class Note(NoteInDBBase):
    pass
