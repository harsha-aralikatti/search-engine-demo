# src/models/product.py
"""
SQLAlchemy database model for Product.

This table stores all product metadata along with
behavioral interaction metrics (clicks, carts, purchases, etc.)
which are later used for ranking during search.
"""

from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Product(Base):
    """
    Represents a product stored in PostgreSQL.

    This model keeps:
    - Core product details (title, description, category, etc.)
    - Searchable attributes (stored as JSON)
    - Behavioral metrics used for ranking
    """

    __tablename__ = "products"

    # Primary identifier (UUID stored as string)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Basic product metadata
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float, default=0.0)

    # Additional flexible attributes (e.g., brand, specs)
    attributes = Column(JSON)

    # Behavioral data for ranking algorithms
    click_count = Column(Integer, default=0)
    cart_count = Column(Integer, default=0)
    purchase_count = Column(Integer, default=0)
    total_dwell_time = Column(Float, default=0.0)
    bounce_count = Column(Integer, default=0)

    # Timestamps for record tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
