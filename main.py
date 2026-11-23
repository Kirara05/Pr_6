from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqladmin import Admin, ModelView
from database.connections import conn, engine
from models.events import Event
from models.users import User
from routes.users import user_router
from routes.events import event_router
from routes.web import web_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn()
    yield


app = FastAPI(title="Event Planner (SQLite)", lifespan=lifespan)

# Подключаем готовую веб-админку (откроется по адресу /admin)
admin = Admin(app, engine)


class EventAdmin(ModelView, model=Event):
    name = "Событие"
    name_plural = "События"
    column_list = [Event.id, Event.title, Event.location, Event.tags]


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [User.id, User.email]


admin.add_view(EventAdmin)
admin.add_view(UserAdmin)

# Подключаем сайт и API
app.include_router(web_router)
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
