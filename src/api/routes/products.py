# src/api/routes/products.py
"""
Product ingestion endpoints.

This module exposes the API route used to ingest product
data in bulk from JSON input. It stores the products in
PostgreSQL and then indexes them in Qdrant for semantic search.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.database import get_db
from src.models.schemas import ProductIn
from src.services.ingestion_service import IngestionService

router = APIRouter()


@router.post("/ingest/json")
async def ingest_products(
    products: List[ProductIn],
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest a list of products.

    Flow:
    1. Validate & parse input JSON into Pydantic models.
    2. Save products to PostgreSQL.
    3. Generate embeddings for each product.
    4. Index embeddings in Qdrant for semantic search.
    """
    result = await IngestionService.ingest_products(products, db)
    return result
