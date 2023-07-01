from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.events import Event, EventUpdate
from database.connection import get_session
from sqlmodel import select

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=List[Event])
async def get_events(session=Depends(get_session)) -> List[Event]:
    stmt = select(Event)
    events = session.exec(stmt).all()
    return events


@event_router.get("/{id}", response_model=Event)
async def get_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@event_router.post("/")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "event created successfully"}


@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: int, new_data: EventUpdate, session=Depends(get_session)
) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)

        session.add(event)
        session.commit()
        session.refresh(event)

        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()

        return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="event not found")
