# 📚 LangChain Study Notes

## 1. Accessing ChatGPT & Basic Chain (42 min)
**Video**: [YouTube](https://www.youtube.com/watch?v=7L0MnVu1KEo)

### Implementations
| File | Purpose |
|------|---------|
| **`a1_simplest_gpt_call.py`** | Minimal translation chain using **ChatPromptTemplate**, **ChatOpenAI**, and **StrOutputParser**. Receives a target language plus user text and returns the translation. |
| **`buyer_lc_server.py`** | FastAPI wrapper that exposes the same chain as an HTTP endpoint via **LangServe**. Launches with Uvicorn and serves:<br>• `POST /tradutor/invoke` — JSON body `{"idioma": "<lang>", "texto": "<text>"}` returns the translation.<br>• `GET /tradutor/playground` — interactive UI for quick tests. |

### Run locally
```bash
    uvicorn buyer_lc_server:app --host localhost --port 8000
```

### Example request
```bash
    curl -X POST http://localhost:8000/tradutor/invoke \
         -H "Content-Type: application/json" \
         -d '{"idioma":"french","texto":"Hello, world! How are you?"}'
```

---

## 2. Building a Simple RAG (21 min)
**Video**: [YouTube](https://www.youtube.com/watch?v=lAtA2nCTfF0)  
**Notebook**: [GitHub](https://github.com/infoslack/youtube/blob/main/rag-chatbot/rag_chatbot.ipynb)

### Implementation: `a2_simple_rag.py`
Illustrates step‑by‑step evolution toward Retrieval‑Augmented Generation:

1. Plain question–answering.
2. Manual context enrichment.
3. Additional context with domain knowledge.
4. Full RAG: loads a chunked ArXiv dataset, embeds documents with **OpenAIEmbeddings**, stores them in an in‑memory **Qdrant** vector store, retrieves the most relevant chunks, and injects them into the prompt for a richer answer.

---

## 3. Conversation History & Parallel Execution (single lecture)
### Implementation: `a3_message_history.py`
A simple CLI chatbot that preserves the entire message history (system, user, and assistant messages) to maintain conversational context across turns.

### Implementation: `a4_parallel.py`
Demonstrates **RunnableParallel** to evaluate a product from two perspectives simultaneously:

* One branch lists **pros** of the product’s features.  
* The other branch lists **cons**.  
* Results are merged into a single, neatly formatted response using **RunnableLambda**.

### Implementation: `a5_branching.py`
This example shows how to **route** user feedback to different response strategies with `RunnableBranch`.

1. A first chain classifies the feedback as **positive**, **negative**, **neutral**, or **escalate** (needs a human).
2. `RunnableBranch` evaluates the classification result and forwards the feedback to the matching prompt template.
3. Each prompt generates an appropriate reply, so the entire flow returns a tailored response for any feedback type.

The demo input `"Preciso de ajuda com o produto, não consigo resolver o problema."` is classified as *escalate* and triggers a message that hands the case to human support.
