from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class Role(BaseModel):
    id: str
    name: str
    description: str

class User(BaseModel):
    sub: str
    given_name: str
    family_name: str
    nickname: str
    name: str
    picture: str
    updated_at: datetime
    email: EmailStr
    email_verified: bool
    roles: Optional[List[Role]] = None
