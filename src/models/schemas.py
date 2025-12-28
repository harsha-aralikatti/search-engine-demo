# src/models/schemas.py
"""
Pydantic schemas for request validation.

These models enforce the structure and type-safety of incoming
API data before saving to the database or indexing in Qdrant.
"""

from pydantic import BaseModel
from typing import Dict, Optional


class ProductIn(BaseModel):
    """
    Input schema for ingesting products via API.

    This represents the raw data received in POST /ingest/json.
    """
    title: str
    description: str
    category: str
    price: float
    rating: float
    attributes: Dict


class EventIn(BaseModel):
    """
    Schema for capturing user behavior events such as:
    - click
    - add-to-cart
    - purchase
    - dwell (time spent)

    These events are used to improve ranking algorithms.
    """
    event_type: str            # click, cart, purchase, dwell
    product_id: str
    dwell_time: Optional[float] = None
