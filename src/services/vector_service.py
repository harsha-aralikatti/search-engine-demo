# src/services/vector_service.py
"""
Handles all Qdrant vector database operations:
- Create collection
- Insert product embeddings
- Perform vector search
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from src.core.config import settings
import uuid

# Name of the vector collection inside Qdrant
COLLECTION_NAME = "products_collection"


def get_qdrant_client():
    """
    Returns an instance of QdrantClient connected to local Qdrant.
    """
    return QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )


def init_qdrant_collection():
    """
    Ensures a clean Qdrant collection with a single unnamed vector field.

    Qdrant 1.x (OLD API) supports only:
        vector=[...]    → NOT named
    So we recreate the collection in that format.
    """
    client = get_qdrant_client()

    # Delete old collection to avoid schema mismatch
    collections = client.get_collections().collections
    if COLLECTION_NAME in [c.name for c in collections]:
        client.delete_collection(COLLECTION_NAME)

    # Create NEW collection with the correct vector dimensions
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=qmodels.VectorParams(
            size=settings.EMBEDDING_DIM,       # Must match embedding model dim
            distance=qmodels.Distance.COSINE   # Cosine similarity for search
        )
    )

    print("✅ Collection created with OLD API format (single vector field).")


def vector_upsert(product_id: str, vector: list, payload: dict):
    """
    Insert/Update a vector embedding into Qdrant.

    Args:
        product_id: Unique product UUID (also used as point ID)
        vector: Embedding list (length = EMBEDDING_DIM)
        payload: Metadata stored along with the vector
    """
    client = get_qdrant_client()

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            qmodels.PointStruct(
                id=product_id,                 # Using product DB ID for consistency
                vector=vector,                 # OLD API → must use `vector=` field
                payload={**payload, "product_id": product_id}
            )
        ]
    )


async def vector_search(query_vector: list, limit: int = 5):
    """
    Performs vector similarity search inside Qdrant.

    Args:
        query_vector: Embedding of the search text
        limit: How many similar products to return

    Returns:
        List of ScoredPoint objects
    """
    client = get_qdrant_client()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,    # Vector to search against
        limit=limit
    )

    return results
