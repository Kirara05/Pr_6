from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(tags=["Events"])


# 1. CREATE: Сохранение нового события в БД
@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(
    new_event: Event, session: Session = Depends(get_session)
) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Событие успешно сохранено в SQLite!"}


# 2. READ: Получение всех событий из БД
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events


# 3. READ: Получение события по ID из БД
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено!",
        )
    return event


# 4. UPDATE: Обновление события в БД
@event_router.put("/edit/{id}", response_model=Event)
async def update_event(
    id: int, new_data: EventUpdate, session: Session = Depends(get_session)
) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено!"
        )
    event_data = new_data.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(event, key, value)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


# 5. DELETE: Удаление события из БД
@event_router.delete("/delete/{id}")
async def delete_event(id: int, session: Session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено!"
        )
    session.delete(event)
    session.commit()
    return {"message": "Событие успешно удалено из БД!"}
