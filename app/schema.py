from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime


class PostDt(BaseModel):
    title:str
    content:str
    published:bool = True 

class CreatePostDt(PostDt):
   pass


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True


class PostResponse(PostDt):
    id:int
    owner_id:int
    owner:UserOut
    title:str
    votes:str
    content:str
    published:bool
    created_at:datetime
    class Config:
        orm_mode = True

class PostOut(PostDt):
    post:PostResponse
    votes:int
# User interface

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokeData(BaseModel):
    id:Optional[str] = None


class Vote(BaseModel):
    post_id:int
    dir : conint(le=1) # type: ignore