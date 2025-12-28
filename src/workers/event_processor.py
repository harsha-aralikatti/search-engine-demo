# src/workers/event_processor.py

import asyncio
import json
import redis
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import AsyncSessionLocal
from src.core.config import settings
from src.models.product import Product
from src.models.event import UserEvent


EVENT_STREAM = "user_events"


# --------------------------------------
# Redis client
# --------------------------------------
def get_redis_client():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )


# --------------------------------------
# Event Processing Logic
# --------------------------------------
async def process_event(event_data: dict, db: AsyncSession):

    # Save raw event to DB
    event = UserEvent(
        id=event_data.get("id"),
        user_id=event_data.get("user_id"),
        session_id=event_data.get("session_id"),
        event_type=event_data.get("event_type"),
        query=event_data.get("query"),
        product_id=event_data.get("product_id"),
        event_data=event_data.get("metadata"),
    )
    db.add(event)

    # Update product behavioral signals
    product_id = event_data.get("product_id")
    if product_id:
        stmt = select(Product).where(Product.id == product_id)
        product = (await db.execute(stmt)).scalar_one_or_none()

        if product:
            if event_data["event_type"] == "click":
                product.click_count += 1

            elif event_data["event_type"] == "add_to_cart":
                product.cart_count += 1

            elif event_data["event_type"] == "purchase":
                product.purchase_count += 1

            elif event_data["event_type"] == "dwell":
                dwell = event_data.get("metadata", {}).get("seconds", 0)
                product.total_dwell_time += dwell

            elif event_data["event_type"] == "bounce":
                product.bounce_count += 1

    await db.commit()


# --------------------------------------
# Worker Loop
# --------------------------------------
async def event_worker():
    print("🚀 Event Processor Started... Listening on Redis Stream")
    redis_client = get_redis_client()

    last_id = "0-0"     # read from beginning

    while True:
        messages = redis_client.xread(
            {EVENT_STREAM: last_id},
            block=5000,   # wait 5 seconds
            count=10
        )

        if messages:
            stream, events = messages[0]

            async with AsyncSessionLocal() as db:
                for event_id, payload in events:
                    data = json.loads(payload["data"])

                    await process_event(data, db)

                    last_id = event_id

        await asyncio.sleep(0.1)


# --------------------------------------
# Entry Point
# --------------------------------------
if __name__ == "__main__":
    asyncio.run(event_worker())
