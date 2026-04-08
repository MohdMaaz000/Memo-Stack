from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    type: Optional[str] = "access"
