# src/api/routes/search.py
"""
Search endpoints for contextual and semantic retrieval.

This module exposes:
1. Standard contextual search combining DB filters + vector ranking.
2. Raw semantic search directly using query embeddings on Qdrant.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.services.search_service import SearchService
from src.services.vector_service import vector_search
from src.core.embeddings import generate_local_embedding

router = APIRouter()   # No prefix here; prefix applied in main.py


# ------------------------------------------------------------
# 1) HYBRID SEARCH (DB filtering + vector ranking)
# ------------------------------------------------------------
@router.get("/")
async def search(
    q: str,
    category: str = None,
    price_min: float = None,
    price_max: float = None,
    rating_min: float = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Performs hybrid product search.

    Steps:
    1. Embedding → Qdrant vector search.
    2. Get matching product IDs.
    3. Fetch corresponding rows from DB.
    4. Apply filters (category, price, rating).
    5. Apply behavioral + semantic ranking.
    """
    results = await SearchService.search(
        db=db,
        query=q,
        category=category,
        price_min=price_min,
        price_max=price_max,
        rating_min=rating_min,
    )
    return results


# ------------------------------------------------------------
# 2) PURE SEMANTIC SEARCH (for testing / debugging)
# ------------------------------------------------------------
@router.post("/semantic")
async def semantic_search(query: str, limit: int = 5):
    """
    Direct semantic search without DB involvement.

    Useful for:
    - Testing embeddings
    - Verifying Qdrant vector results

    Steps:
    1. Convert query text → embedding.
    2. Run vector search against Qdrant.
    """
    vector = await generate_local_embedding(query)
    results = await vector_search(vector, limit)
    return results
