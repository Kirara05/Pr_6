from fastapi import APIRouter, HTTPException, status, Body
from models.events import Event
from typing import List

event_router = APIRouter(tags=["Events"])
events_db = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events_db


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events_db:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Событие с указанным ID не найдено!",
    )


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event = Body(...)) -> dict:
    events_db.append(body)
    return {"message": "Событие успешно создано!"}


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events_db:
        if event.id == id:
            events_db.remove(event)
            return {"message": "Событие успешно удалено!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Событие с указанным ID не найдено!",
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events_db.clear()
    return {"message": "Все события успешно удалены!"}
