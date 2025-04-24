## 🗂️ Quotation-Matcher Subsystem

This micro-service receives a **POST** request with raw quotation items (free-text description, size and price) and responds with the same items enriched with the **internal `sku_id`** found via vector similarity search in a local Qdrant collection.

---

### 1. Business Purpose
| Goal | Why it matters |
|------|----------------|
| **Normalize supplier quotes** | Suppliers never know your SKU codes. The service maps their wording to your canonical catalog. |
| **Guarantee consistency** | Every downstream process (pricing rules, ERP, stock updates) relies on the master `sku_id`. |
| **Keep fast & local** | All data lives in a local Qdrant instance—no cloud latency or extra cost. |

---

### 2. High-Level Flow
```
┌────────────┐  HTTP POST /match
│  BuyerAPI  │  [{ description, brand?, size_value, unit, price }]
└─────┬──────┘
      │
      ▼
┌────────────┐       1. generate embedding
│  FastAPI   │───┐   2. similarity_search in Qdrant (collection: skus)
│  (Python)  │   │   3. choose best match (optionally apply filters)
└─────┬──────┘   │
      │          │
      ▼          │
┌────────────┐◄──┘
│   Qdrant   │
└────────────┘
      │
      ▼
HTTP 200 OK  →  [{ sku_id, price, confidence }]
```

---

### 3. Tech Stack
| Layer | Choice |
|-------|--------|
| Runtime | **Python 3.12** |
| Web framework | **FastAPI** |
| Embeddings | `text-embedding-3-small` (OpenAI) |
| Vector store | **Qdrant** (local / persisted under `./qdrant_storage`) |
| Dependency management | `poetry` or `pip + requirements.txt` |
| Container | `Dockerfile` provided (optional) |

---

### 4. API Contract

#### `POST /match`

```jsonc
// Request body
{
  "cart_id": "c50eb6e5-f38c-42cf-8e76-5bf1b4d1e96b",
  "items": [
    {
      "description": "Chicken wings",
      "brand": "Seara",
      "size_value": 5.0,
      "unit": "kg",
      "price": 12.8,
      "product_type": "Carne de Frango"
    }
  ]
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `cart_id` | string (uuid) | yes | Used to filter the Cart items collection |
| `items[]` | array | yes | One or more quotation lines |

```jsonc
// Successful response
{
  "items": [
    {
      "sku_id": "F896F57D-CC4A-427A-B716-648932FB65E0",
      "price": 12.8,
      "confidence": 0.93
    }
  ]
}
```

*HTTP codes*

| Code | Meaning |
|------|---------|
| `200 OK` | All items matched (or partially matched, see body) |
| `207 Multi-Status` | Some items unmatched; field `unmatched[]` returned |
| `400 Bad Request` | Invalid payload |
| `500 Internal Server Error` | Unexpected failure (e.g. Qdrant offline) |

---

### 5. Setup & Run - does not work yet

```bash
# 1. install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. prepare environment
cp .env.example .env          # add OPENAI_API_KEY
python scripts/index_skus.py  # loads input.json → Qdrant

# 3. start the service
uvicorn app.main:api --host 0.0.0.0 --port 8000
```

Optional Docker:

```bash
docker compose up --build
```

---

### 6. Indexing New SKUs - not done
Run the helper whenever the catalog changes:

```bash
python scripts/index_skus.py --file data/new_skus.json
```

The script **upserts** documents; existing `sku_id`s are updated, new ones are appended.

---

### 7. Tuning Similarity -- will do

| Parameter | Default | Effect |
|-----------|---------|--------|
| `k` | `5` | Candidates retrieved before scoring |
| `min_score` | `0.40` | Threshold below which the item is flagged *unmatched* |
| `filters` | brand / unit / size_value | Improve precision when duplicates exist |

Adjust in `settings.py`.

---

### 8. Roadmap - not sure about this
- **Batch endpoint** for nightly catalog sync  
- **Feedback loop**: store wrong matches and fine-tune filtering rules  
- **Supplier-specific synonyms** collection  
- **Auth** (JWT) once exposed outside the cluster

---

### 9. License
MIT – see `LICENSE`.