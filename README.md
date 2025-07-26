# **LangChain Playground**

> ⚠️ This repository is **NOT** the production Buyer-API.  
> It only hosts **proof-of-concept** Python scripts for studying LangChain, Qdrant, and FastAPI.  
> The real implementation (Cart CRUD, Quotation-Matcher, full RAG) will live in a private repository.

---

## 📂 Project Layout

```
.
├── a_overview/               # Step-by-step demos from tutorials
│   ├── a1_simplest_gpt_call.py
│   ├── a1_fast_api.py
│   ├── a2_simple_rag.py
│   ├── a3_message_history.py
│   ├── a4_parallel.py
│   └── a5_branching.py
│
├── buyer/                    # Integrated experiments
│   ├── database/
│   │   └── qdrant_storage/   # Vector store (created at runtime)
│   ├── input.json            # Mock SKU data
│   ├── seed_database.py      # Populates the cart_items collection
│   ├── main.py               # CLI for testing the Quotation-Matcher
│   └── all_logic_but_does_not_work.py
│
├── langchain_study_notes.md  # Extended study notes (source for this README)
└── core_concepts.md          # General notebook-style notes
```

---

## 🔧 Quick Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # langchain, qdrant-client, fastapi, uvicorn...
cp .env.example .env                     # add your OPENAI_API_KEY
```

---

## 🚀 Available Demos

| Script | Highlights | How to run |
|--------|------------|------------|
| **`a_overview/a1_simplest_gpt_call.py`** | Minimal GPT call via LangChain | `python a_overview/a1_simplest_gpt_call.py` |
| **`a_overview/a1_fast_api.py`** | Wraps the same chain in FastAPI + LangServe | `uvicorn a_overview.a1_fast_api:app --reload`   → `POST /tradutor/invoke` |
| **`a_overview/a2_simple_rag.py`** | Incremental RAG build using an in-memory Qdrant | `python a_overview/a2_simple_rag.py` |
| **`buyer/main.py`** | Terminal Quotation-Matcher prototype saving items to `cart_items` | `python buyer/main.py` |

Detailed explanations live in **`langchain_study_notes.md`**.

---

## ✅ What *is* implemented

1. **Embeddings & GPT chains** — prompt templates, parallel and branching flows.  
2. **FastAPI + LangServe** — translation endpoint with auto-generated Swagger UI.  
3. **Simple RAG** — loads a chunked ArXiv dataset, embeds with OpenAI, stores in Qdrant, retrieves context.  
4. **CLI Quotation-Matcher** — extracts item data with GPT, matches to SKU IDs via Qdrant similarity search, prints a quote.

> **Limitations**  
> - No authentication, error handling, or automated tests.  
> - Prototype code only—**not** production-grade.

---

## 📌 Next Steps (handled in the private repo)

| Feature | Target repo |
|---------|-------------|
| Full Cart CRUD REST | **Buyer-API (private)** |
| `/match` Quotation-Matcher service | idem |
| Persistent RAG with conversation history | idem |
| Docker-compose, CI/CD pipeline | idem |

---

**License**: MIT (for this playground).
