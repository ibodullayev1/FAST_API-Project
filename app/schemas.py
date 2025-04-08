from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
