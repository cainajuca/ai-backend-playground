from dotenv import load_dotenv
import json
from pathlib import Path
from typing import List, Dict

from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

from database.repositories.cart_repository import insert_cart, fetch_cart
from buyer.database.repositories.common_repository import ensure_collection

# ---------- Configuration ----------
load_dotenv() # needs OPENAI_API_KEY
DATA_PATH = Path(__file__).parent
SKUS_FILE = DATA_PATH / "input.json"
QDRANT_PATH = DATA_PATH / "qdrant_storage"
COLLECTION_NAME = "cart_items"
EMBED_MODEL_NAME = "text-embedding-3-small"

# ---------- Initializes embeddings ----------
embeddings = OpenAIEmbeddings(model=EMBED_MODEL_NAME)
client      = QdrantClient(path=str(QDRANT_PATH))

def load_skus() -> List[Dict]:
    with open(SKUS_FILE, encoding="utf-8") as f:
        return json.load(f)
    
def print_cart(cart_id, items):
    print(f"\nThe cart {cart_id} has {len(items)} SKUs:\n")
    for p in items:
        meta = p.payload["metadata"]
        print(" •", meta["sku_id"], "| brand:", meta["brand"], 
          "| description:", meta["description"],
          "| size:", meta["size_value"], meta["unit"])
    print() # break line

# ---------------------- MAIN ----------------------

cart_id = "3569CC05-9165-461A-893D-5B48EA8BAA7D" # real Cart
# cart_id = "D669C632-FF68-4899-9F00-BE7498724DC9" # fake Cart for testing

ensure_collection(client, COLLECTION_NAME)
items = fetch_cart(cart_id, client, COLLECTION_NAME)

if len(items) == 0:
    skus_data = load_skus()
    insert_cart(cart_id, skus_data, client, embeddings, COLLECTION_NAME)

items = fetch_cart(cart_id, client, COLLECTION_NAME)
print_cart(cart_id, items)
