
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

def ensure_collection(client: QdrantClient, collection_name: str):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created.")