from sqlmodel import SQLModel, Field
from typing import Optional


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    location: Optional[str] = ""
    description: Optional[str] = ""
    tags: Optional[str] = ""
    image: Optional[str] = ""


class EventUpdate(SQLModel):
    title: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    image: Optional[str] = None
