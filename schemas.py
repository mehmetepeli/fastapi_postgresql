from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional


# Pydantic model for request validation
class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: str = "user"

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    published_date: str
    rating: int
    user_id: int

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    published_date: Optional[str] = None
    rating: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class MovieCreate(BaseModel):
    title: str
    director: str
    genre: str
    release_date: str
    rating: int
    user_id: int

    class Config:
        from_attributes = True

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    release_date: Optional[str] = None
    rating: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class BoardGameCreate(BaseModel):
    title: str
    designer: str
    genre: str
    release_date: str
    user_id: int

    class Config:
        from_attributes = True

class BoardGameUpdate(BaseModel):
    title: Optional[str] = None
    designer: Optional[str] = None
    genre: Optional[str] = None
    release_date: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class ComicCreate(BaseModel):
    title: str
    author: str
    genre: str
    published_date: str
    user_id: int

    class Config:
        from_attributes = True

class ComicUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    published_date: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True