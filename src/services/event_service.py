# src/services/event_service.py

import json
import redis
from src.core.config import settings


EVENT_STREAM = "user_events"


def get_redis_client():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )


class EventService:

    @staticmethod
    def push_event(event: dict):
        """
        Push an event into Redis Stream for async processing.
        """

        redis_client = get_redis_client()

        redis_client.xadd(
            EVENT_STREAM,
            {
                "data": json.dumps(event)
            }
        )

        return {"status": "queued", "event": event}
