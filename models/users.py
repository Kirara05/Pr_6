from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str


class NewUser(BaseModel):
    email: EmailStr
    password: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
