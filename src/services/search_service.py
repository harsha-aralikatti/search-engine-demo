# src/services/search_service.py
"""
Search service responsible for:
1. Creating embeddings for user queries
2. Running vector similarity search in Qdrant
3. Fetching matching products from the database
4. Applying optional filters
5. Re-ranking results using behavioral signals
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.product import Product
from src.core.embeddings import generate_local_embedding
from src.services.vector_service import vector_search
from src.services.learning_service import apply_behavioral_ranking


class SearchService:
    """
    Orchestrates the entire search pipeline:
    - Embedding
    - Vector search
    - DB filtering
    - Behavioral re-ranking
    """

    @staticmethod
    async def search(
        db: AsyncSession,
        query: str,
        category: str = None,
        price_min: float = None,
        price_max: float = None,
        rating_min: float = None,
        limit: int = 10
    ):
        """
        Executes a complete product search workflow.

        Args:
            db: AsyncSession for database interaction
            query: User search input
            category: Optional category filter
            price_min/max: Optional price filters
            rating_min: Optional rating filter
            limit: Number of results to return

        Returns:
            Ranked list of Product objects with additional scoring metadata
        """

        # STEP 1 — Convert query text to embedding vector
        query_embedding = generate_local_embedding(query)

        # STEP 2 — Retrieve similar products from Qdrant
        qdrant_results = await vector_search(query_embedding, limit=limit)

        # Extract product IDs and similarity scores
        candidate_ids = [str(hit.id) for hit in qdrant_results]
        similarity_map = {str(hit.id): hit.score for hit in qdrant_results}

        if not candidate_ids:
            return []

        # STEP 3 — Fetch matching product objects from DB
        stmt = select(Product).where(Product.id.in_(candidate_ids))
        products = (await db.execute(stmt)).scalars().all()

        # STEP 4 — Apply all optional filters
        filtered = []
        for p in products:
            if category and p.category != category:
                continue
            if price_min and p.price < price_min:
                continue
            if price_max and p.price > price_max:
                continue
            if rating_min and p.rating < rating_min:
                continue
            filtered.append(p)

        # STEP 5 — Apply behavior + similarity combined ranking
        # The ranking function enhances relevance based on:
        # - similarity score (from vector search)
        # - user behavior signals (clicks, purchases, dwell time, bounce)
        ranked = apply_behavioral_ranking(filtered, similarity_map)

        return ranked
