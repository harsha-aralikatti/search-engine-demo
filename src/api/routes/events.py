# src/api/routes/events.py

from fastapi import APIRouter
from src.models.schemas import EventIn
from src.services.event_service import EventService
import uuid

router = APIRouter()

@router.post("/")
async def push_event(event: EventIn):
    event_dict = event.dict()
    event_dict["id"] = str(uuid.uuid4())

    EventService.push_event(event_dict)
    return {"status": "queued", "event": event_dict}
