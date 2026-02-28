from pydantic import BaseModel, Field, field_validator, computed_field, EmailStr
from functools import cached_property
from datetime import datetime as dati
from typing import List

class UserUpdate(BaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    bio_info: str = Field(default=None)
    email: EmailStr = Field(default=None)

class UserCreate(UserUpdate):
    nickname: str
    password: str

class UserOut(UserUpdate):
    id: int
    nickname: str
    active: bool
    date_joined: dati

    class Config:
        from_attributes = True


class CategoryUpdateAndCreate(BaseModel):
    slug: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    is_published: bool = Field(default=None)

class CategoryOut(CategoryUpdateAndCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True


class LocationUpdateAndCreate(BaseModel):
    name: str = Field(default=None)
    is_published: bool = Field(default=None)

class LocationOut(LocationUpdateAndCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: str = Field(default=None)
    text: str = Field(default=None)
    pub_date: dati = Field(default=None)
    is_published: bool = Field(default=None)
    image: str = Field(default=None)
    location_id: int = Field(default=None)
    category_id: int = Field(default=None)

class PostCreate(PostUpdate):
    author_id: int = Field(default=None)

class PostOut(PostCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True

class PostDetail(PostOut):
    author: UserOut
    category: CategoryOut = Field(default=None)
    location: LocationOut = Field(default=None)
    comments: List["CommentOut"] = Field(default=[])

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    text: str = Field(default=None)

class CommentCreate(CommentUpdate):
    post_id: int
    author_id: int

class CommentOut(CommentCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True