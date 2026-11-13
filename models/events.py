from sqlmodel import SQLModel, Field
from typing import Optional


# 1. Модель таблицы в БД
class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str | None = None
    description: str
    tags: str | None = None
    location: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Открытие фестиваля",
                "image": "https://linktomyimage.com/image.png",
                "description": "Презентация и открытие главной сцены фестиваля",
                "tags": "festival, music, open-air",
                "location": "Главная сцена",
            }
        }


class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    location: Optional[str] = None
