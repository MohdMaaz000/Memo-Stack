from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    content: Optional[str] = None

class CommentInDBBase(CommentBase):
    id: int
    note_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class Comment(CommentInDBBase):
    pass
