from dotenv import load_dotenv
import json, os, uuid
from pathlib import Path
from typing import List, Dict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

# ---------- Configuração ----------
load_dotenv()                                   # precisa do OPENAI_API_KEY
DATA_PATH = Path(__file__).parent
SKUS_FILE = DATA_PATH / "skus.json"
QDRANT_PATH = DATA_PATH / "qdrant_storage"
EMBED_MODEL_NAME = "text-embedding-3-small"

# ---------- 1. Inicializa embeddings ----------
embeddings = OpenAIEmbeddings(model=EMBED_MODEL_NAME)

# ---------- 2. Indexa / atualiza coleção de SKUs ----------
def load_skus() -> List[Dict]:
    with open(SKUS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def upsert_skus_into_qdrant(skus: List[Dict]):
    client = QdrantClient(path=str(QDRANT_PATH))
    # cria a collection se ainda não existir
    if "skus" not in [c.name for c in client.get_collections().collections]:
        Qdrant.from_documents(
            documents=[],
            embedding=embeddings,
            location=str(QDRANT_PATH),
            collection_name="skus",
        )
    # carrega vetor store
    sku_store = Qdrant(
        client=client,
        embeddings=embeddings,
        collection_name="skus"
    )
    # prepara docs
    from langchain_core.documents import Document
    docs = []
    for s in skus:
        page_text = (
            f"{s['description']} {s['brand']} "
            f"{s['size_value']} {s['unit']} {s['product_type']}"
        )
        docs.append(Document(page_content=page_text, metadata=s))
    sku_store.add_documents(docs)

skus_data = load_skus()
upsert_skus_into_qdrant(skus_data)

# ---------- 2b. Verifica se a coleção foi criada corretamente ----------
from qdrant_client import QdrantClient
client = QdrantClient(path="qdrant_storage")
total = client.count(collection_name="skus", exact=True).count
print("Total de SKUs:", total)

# ---------- 3. Abre as coleções ----------
client = QdrantClient(path=str(QDRANT_PATH))
sku_store = Qdrant(client=client, embeddings=embeddings, collection_name="skus")

conversation_id = str(uuid.uuid4()) # future supplier_id
conv_store = Qdrant.from_documents(
    documents=[],
    embedding=embeddings,
    location=str(QDRANT_PATH),
    collection_name="conversations",
)  # if exists it just opens

# ---------- 4. Loop de chat ----------
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

quotation: Dict[str, float] = {}

EXTRACT_SYSTEM = SystemMessage(
    content=(
        "Você é um assistente que extrai itens de cotação em JSON. "
        "Retorne sempre no formato "
        "[{\"description\":\"...\",\"brand\":\"...\",\"unit\":\"...\","
        "\"size_value\":NUM, \"quantity\":NUM, \"price\":NUM}]. "
        "Se não encontrar algum campo, deixe string vazia ou 0."
    )
)

print("🟢 Chat iniciado. Digite mensagens do fornecedor. Insira 'fim' para encerrar.\n")

while True:
    user_input = input("> ").strip()
    if user_input.lower() == "fim":
        break
    if not user_input:
        continue

    # Salva a mensagem na collection de conversa
    conv_store.add_texts([user_input], metadatas=[{"conversation_id": conversation_id}])

    # ---------- 4a. Extrai itens ----------
    msgs = [EXTRACT_SYSTEM, HumanMessage(content=user_input)]
    try:
        extraction = llm.invoke(msgs).content
        items = json.loads(extraction)
    except Exception as e:
        print("⚠️  Não consegui extrair itens:", e)
        continue

    # ---------- 4b. Faz matching de cada item ----------
    for item in items:
        query = (
            f"{item['description']} {item['brand']} "
            f"{item['size_value']} {item['unit']}"
        )

        matches = sku_store.similarity_search(query, k=1)
        if not matches:
            print("❌  Não encontrei SKU para:", query)
            continue
        sku_id = matches[0].metadata["sku_id"]
        price = float(item["price"])
        quotation[sku_id] = price
        print(f"✔️  {sku_id}  ->  {price:.2f}")
        # print(f"✔️  id_qualquer  ->  10 real")

# ---------- 5. Resultado final ----------
print("\n📄 Cotação final\n----------------")
for sku, price in quotation.items():
    print(f"{sku:<10} : {price:.2f}")
print("----------------\nFim.\n")
