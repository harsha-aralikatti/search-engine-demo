from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()

class EventType(str, Enum):
    SEARCH = "search"
    CLICK = "click"
    ADD_TO_CART = "add_to_cart"
    PURCHASE = "purchase"
    DWELL = "dwell"
    BOUNCE = "bounce"


class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    event_type = Column(String, nullable=False)

    query = Column(String)
    product_id = Column(String, index=True)

    # rename "metadata" → reserved word in SQLAlchemy
    event_data = Column(JSON)

    timestamp = Column(DateTime, default=datetime.utcnow)
