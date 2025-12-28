from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from src.core.config import settings

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

print("Deleting old collection if exists...")

try:
    client.delete_collection("products_collection")
    print("Deleted.")
except Exception as e:
    print("Collection not found, skipping.")

print("\nCreating new collection with EMBEDDING_DIM =", settings.EMBEDDING_DIM)

client.recreate_collection(
    collection_name="products_collection",
    vectors_config={
        "embedding": qmodels.VectorParams(
            size=settings.EMBEDDING_DIM,
            distance=qmodels.Distance.COSINE
        )
    }
)


print("Collection recreated successfully!")
