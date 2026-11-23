from fastapi import FastAPI
from contextlib import asynccontextmanager
import motor.motor_asyncio
from beanie import init_beanie
from database.connection import Settings
from models.events import Event
from models.users import User
from routes.users import user_router
from routes.events import event_router
from routes.web import web_router
import uvicorn

# Заглушка совместимости Beanie и Motor
motor.motor_asyncio.AsyncIOMotorClient.append_metadata = (
    lambda self, *args, **kwargs: None
)

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=[Event, User]
    )
    yield


app = FastAPI(title="Event Planner", lifespan=lifespan)

app.include_router(web_router)
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
