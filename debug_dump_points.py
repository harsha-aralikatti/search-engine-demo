from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from src.core.config import settings

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

print("\n=== COLLECTION INFO ===")
info = client.get_collection("products_collection")
print(info)

print("\n=== LIST ALL POINT IDS ===")
points = client.scroll(
    collection_name="products_collection",
    limit=50,
    with_payload=True,
    with_vectors=False
)

print(points)
print("\nTotal points:", len(points[0]))
