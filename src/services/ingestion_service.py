# src/services/ingestion_service.py
"""
Ingestion service responsible for:
1. Saving incoming product data to Postgres
2. Generating embeddings for each product
3. Storing vectors + metadata in Qdrant for semantic search
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import Product
from src.models.schemas import ProductIn
from src.core.embeddings import generate_local_embedding
from src.services.vector_service import vector_upsert


class IngestionService:
    """
    Handles end-to-end product ingestion:
    - Database insert
    - Embedding generation
    - Vector store upsert
    """

    @staticmethod
    async def ingest_products(products: list[ProductIn], db: AsyncSession):
        """
        Ingest a batch of products into:
        1. Postgres DB
        2. Qdrant vector store

        Args:
            products: List of ProductIn objects from API
            db: AsyncSession for DB operations

        Returns:
            JSON summary of ingestion status
        """

        stored_products = []

        # STEP 1 — Store raw product records in Postgres
        for p in products:
            product_id = str(uuid.uuid4())

            product = Product(
                id=product_id,
                title=p.title,
                description=p.description,
                category=p.category,
                price=p.price,
                rating=p.rating,
                attributes=p.attributes,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.add(product)
            stored_products.append((product_id, p))

        # Save all records in a single transaction
        await db.commit()

        # STEP 2 — Generate embeddings + upsert vectors into Qdrant
        for product_id, p in stored_products:
            text = f"{p.title} {p.description}"
            embedding = generate_local_embedding(text)

            # Store embedding + metadata in Qdrant
            vector_upsert(
                product_id=product_id,
                vector=embedding,
                payload=p.dict()
            )

        return {
            "message": "Products ingested successfully",
            "count": len(products)
        }
