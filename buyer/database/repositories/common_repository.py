
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

def ensure_collection(client: QdrantClient, collection_name: str):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created.")

def any_items(client: QdrantClient, collection_name: str) -> bool:
    """
    Return True if the collection contains at least one point, otherwise False.
    """
    # Qdrant counts the points without bringing vectors or payloads.
    total = client.count(collection_name=collection_name).count
    return total > 0