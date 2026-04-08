from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    is_public: bool = False

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    is_public: Optional[bool] = None

class BookInDBBase(BookBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class Book(BookInDBBase):
    pass
