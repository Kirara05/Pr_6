from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


# Модель пользователя
class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = []


# Модель для регистрации (с именем)
class NewUser(User):
    username: str


# Модель только для входа
class UserSignIn(BaseModel):
    email: EmailStr
    password: str
