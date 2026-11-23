from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connections import get_session
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    return session.exec(select(Event)).all()


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено",
        )
    return event


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event, session: Session = Depends(get_session)) -> dict:
    session.add(body)
    session.commit()
    session.refresh(body)
    return {"message": "Событие успешно создано"}


@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: int, body: EventUpdate, session: Session = Depends(get_session)
) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено",
        )
    event_data = body.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(event, key, value)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@event_router.delete("/{id}")
async def delete_event(id: int, session: Session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено",
        )
    session.delete(event)
    session.commit()
    return {"message": "Событие успешно удалено"}
