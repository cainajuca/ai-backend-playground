### Vector Stores
Databases optimized for **nearest‑neighbor search** over high‑dimensional vectors.  
They let a RAG system quickly retrieve documents whose vector representations are most similar to a query embedding.

### Embeddings
Numeric vectors that encode the **semantic meaning** of text.  
Both queries and chunks are embedded, enabling similarity comparison in the vector store.

### LLMs (Large Language Models)
Transformer‑based models (e.g., GPT‑4) that generate or understand natural language.  
In RAG, the LLM consumes retrieved context + the user prompt to produce an informed answer.

### Chunks
Small, coherent slices of a larger document (paragraphs, sections, etc.).  
Chunking makes retrieval more precise because only the most relevant segments are fetched and supplied to the LLM.

### Tokens
Sub‑word units used by LLMs to process text; they determine **model cost and context length**.  
RAG reduces token usage by retrieving only the most relevant chunks instead of sending entire documents.
