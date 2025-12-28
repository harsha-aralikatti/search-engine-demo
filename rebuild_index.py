from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

client.update_collection(
    collection_name="products_collection",
    optimizer_config={
        "default_segment_number": 1
    }
)

print("Index rebuild triggered!")
