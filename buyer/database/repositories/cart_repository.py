from typing import List, Dict
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from qdrant_client.models import Filter, FieldCondition, MatchValue

def insert_cart(
    cart_id: str,
    skus: List[Dict],
    client: QdrantClient, 
    embeddings: OpenAIEmbeddings,
    collection_name: str):

    store = QdrantVectorStore(
        client=client,
        embedding=embeddings,
        collection_name=collection_name
    )

    docs = [
        Document(
            page_content=f"{s['description']} {s['brand']} "
                         f"{s['size_value']} {s['unit']} {s['product_type']}",
            metadata={**s, "cart_id": cart_id}  # << added
        )
        for s in skus
    ]
    store.add_documents(docs)

def fetch_cart(cart_id: str, client: QdrantClient, collection_name: str):
    flt = Filter(
        must=[
            FieldCondition(
                key="metadata.cart_id",
                match=MatchValue(value=cart_id)
            )
        ]
    )

    points, _ = client.scroll(
        collection_name=collection_name,
        scroll_filter=flt,
        limit=200,
    )

    return points