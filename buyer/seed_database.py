from dotenv import load_dotenv
import json
from pathlib import Path
from typing import List, Dict

from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from database.repositories.cart_repository import insert_cart_batch
from database.repositories.common_repository import ensure_collection, any_items
    
from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

# ---------- Configuração ----------
load_dotenv() # precisa do OPENAI_API_KEY
DATA_PATH = Path(__file__).parent
SKUS_FILE = DATA_PATH / "database/seed/seed_cart_collection.json"
QDRANT_PATH = DATA_PATH / "qdrant_storage"
COLLECTION_NAME = "cart_items"
EMBED_MODEL_NAME = "text-embedding-3-small"

# ---------- Initializes embeddings ----------
embeddings = OpenAIEmbeddings(model=EMBED_MODEL_NAME)
client = QdrantClient(path=str(QDRANT_PATH))

def load_skus() -> List[Dict]:
    with open(SKUS_FILE, encoding="utf-8") as f:
        return json.load(f)

def print_cart(cart_id: str, items: Sequence[PointStruct]) -> None:
    print(f"\nThe cart {cart_id} has {len(items)} SKUs:\n")
    for p in items:
        meta = p.payload["metadata"]
        print(
            " •",
            meta["sku_id"],
            "| brand:",
            meta["brand"],
            "| description:",
            meta["description"],
            "| size:",
            meta["size_value"],
            meta["unit"],
        )
    print() # break line

def fetch_all_carts(client: QdrantClient, collection_name: str, batch: int = 256) -> Dict[str, List[PointStruct]]:
    """
    Iterates through the entire collection and returns a dictionary grouping 
    the points by cart_id.

    Parameters
    ----------
    client : QdrantClient
        The client used to interact with the Qdrant database.
    collection_name : str
        The name of the collection to be queried.
    batch : int, optional
        The number of points to fetch per batch (default is 256).
    Returns
        Key   → cart_id
        Value → List of points that belong to the cart_id
    """
    carts: Dict[str, List[PointStruct]] = defaultdict(list)
    next_offset: Tuple[int, int] | None = None

    while True:
        points, next_offset = client.scroll(
            collection_name=collection_name,
            offset=next_offset, # continues from the last offset
            limit=batch,
        )
        if not points:
            break

        for p in points:
            cart_id = p.payload["metadata"]["cart_id"]
            carts[cart_id].append(p)

        if next_offset is None:
            break

    return carts

# ---------------------- MAIN ----------------------

ensure_collection(client, COLLECTION_NAME)
hasItems = any_items(client, COLLECTION_NAME)

if not hasItems:
    skus_data = load_skus()
    insert_cart_batch(skus_data, client, embeddings, COLLECTION_NAME)

all_carts = fetch_all_carts(client, COLLECTION_NAME)

if not all_carts:
    print("\n⚠️  No carts found in the collection.\n")
else:
    for cart_id, items in all_carts.items():
        print_cart(cart_id, items)