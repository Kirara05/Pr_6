from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from database.connection import Database
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(tags=["Events"])
event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return await event_database.get_all()


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено",
        )
    return event


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {"message": "Событие успешно создано"}


@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено",
        )
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    deleted = await event_database.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено",
        )
    return {"message": "Событие успешно удалено"}
