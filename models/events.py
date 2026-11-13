from pydantic import BaseModel
from typing import List


class Event(BaseModel):
    id: int
    title: str
    image: str | None = None
    description: str
    tags: List[str] | None = None
    location: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Открытие фестиваля (Имя Фамилия)",
                "image": "https://linktomyimage.com/image.png",
                "description": "Презентация и открытие главной сцены фестиваля",
                "tags": ["festival", "music", "open-air"],
                "location": "Главная сцена",
            }
        }
