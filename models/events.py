from beanie import Document
from pydantic import BaseModel
from typing import Optional, List


class Event(Document):
    title: str
    image: Optional[str] = ""
    description: Optional[str] = ""
    tags: Optional[List[str]] = []
    location: Optional[str] = ""

    class Settings:
        name = "events"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Презентация книги",
                "image": "https://site.com/image.png",
                "description": "Обсуждение книги по разработке API",
                "tags": ["python", "fastapi", "book"],
                "location": "Конференц-зал",
            }
        }


class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
