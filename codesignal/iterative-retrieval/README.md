# Iterative Retrieval with Keyword Refinement

A lightweight, cost-effective iterative retrieval engine for RAG pipelines.  
No LLM calls during refinement — just fast regex-based keyword extraction + Chroma vector search.

## Why Iterative Retrieval?

Traditional RAG does one retrieval pass.  
**Iterative retrieval** keeps refining the query using information from the previous retrieval, dramatically improving precision on complex questions.

## Techniques Covered in This Repository

### 1. Naive / One-shot Retrieval

Single embedding lookup → `collection.query(query_texts=[original_query])`.

### 2. Multi-Query Retrieval

Generate 3–5 rephrasings of the original query (via LLM or rules) and union the results.

### 3. HyDE (Hypothetical Document Embeddings)

Ask an LLM to write a hypothetical answer, then embed _that_ answer instead of the question.

### 4. Iterative Refinement (this implementation) ← **Recommended for most use-cases**

- Retrieve best chunk
- Extract new keywords that are **not** already in the current query
- Append them → new query
- Repeat (with early stopping on similarity improvement)

### 5. Other popular variants (not implemented here)

- Step-back prompting
- Self-RAG / corrective retrieval
- LLM-based query rewriting / expansion

## How the Keyword-Based Iterative Technique Works

1. Start with the user query.
2. Retrieve the single best chunk (Chroma cosine distance).
3. Convert distance → similarity score (`1 / (1 + distance)`).
4. If the score improved by at least `IMPROVEMENT_THRESHOLD` (default 0.02):
   - Extract up to **2** new keywords from the chunk (longest first, ≥5 chars, not stopwords, not already in query).
   - Append each keyword to the query **sequentially**.
5. Repeat up to `steps` (default 3) or until no improvement / no new keywords.
6. Return **all** retrieved chunks (one per iteration) as the final context.

This approach is extremely fast, deterministic, and works well even with small chunks (size 40 in the demo).

## Project Structure
```

iterative_retrieval/
├── iterative_retrieval.py # ← main logic (the file you see)
├── data.py # load_and_chunk_corpus
├── vector_db.py # build_chroma_collection
└── data/
└── corpus.json

````

## Quick Start

```bash
pip install chromadb
python iterative_retrieval.py
````

The script runs a live demo on a small policy corpus and prints the refined queries + final combined context.

## Configuration

```python
IMPROVEMENT_THRESHOLD = 0.02   # set to 0.0 to never stop early
STOPWORDS                  # customize if needed
```

## Advantages

- Zero extra LLM cost during retrieval
- Interpretable (you see every keyword that was added)
- Early stopping prevents diminishing returns
- Works with any embedding model (sentence-transformers, OpenAI, etc.)

## Limitations & Future Improvements

- Relies on keywords actually appearing in the chunk
- No semantic understanding of the chunk (could be replaced by LLM summary later)
- Only appends keywords (future version could do full query rewriting)


---

**Detailed explanation of the code**

The script is a **complete, self-contained implementation** of the keyword-based iterative retrieval technique described above. Here is a function-by-function breakdown:

### Constants & Helpers

```python
IMPROVEMENT_THRESHOLD = 0.02
STOPWORDS = set([...])
````

- `IMPROVEMENT_THRESHOLD`: minimum similarity gain required to continue refining. Prevents useless extra steps.
- `STOPWORDS`: classic English stop-word list so we don’t add “the”, “and”, etc.

### `retrieve_best_chunk(...)`

- Performs a **single** Chroma query for the current text.
- Returns the top chunk’s text, a normalised similarity score (`1 / (1 + distance)`), and its metadata.
- Simple but effective conversion from Chroma’s raw distance to a [0,1] similarity.

### `extract_refinement_keywords(chunk_text, current_query, max_keywords=2)`

- Uses regex `\b\w+\b` to split the chunk into words.
- Filters out:
  - stopwords
  - words already present in the current query
  - words shorter than 5 characters
- Returns up to `max_keywords` **unique** candidates, sorted longest-first (so “policy” beats “act”).

### `refine_query(current_query, refine_word)`

- Trivial string concatenation: `"What internal policies..." + " employees"`.

### `iterative_retrieval(query, collection, steps=3)` ← **Core algorithm**

This is where the magic happens:

```python
accumulated_chunks = []
current_query = query
best_score_so_far = 0.0

for step in range(steps):
    # 1. Retrieve
    best_chunk_text, best_chunk_score, metadata = retrieve_best_chunk(...)

    # 2. Early stopping on similarity
    if best_chunk_score - best_score_so_far < IMPROVEMENT_THRESHOLD:
        break
    best_score_so_far = best_chunk_score

    # 3. Save this chunk for final context
    accumulated_chunks.append({...})

    # 4. Extract up to 2 new keywords
    keywords = extract_refinement_keywords(best_chunk_text, current_query, max_keywords=2)

    # 5. Append each keyword (sequential refinement inside the same step)
    for kw in keywords:
        current_query = refine_query(current_query, kw)
```

**Important behaviour**:

- The loop can add **two** keywords per iteration (the `for refine_word in keywords` loop).
- The **next** iteration therefore searches with a query that already contains both new terms.
- The chunk saved is the one retrieved **before** the extra keywords were added.

### `build_final_context(iteration_results)`

- Simple formatter that concatenates every retrieved chunk with its step number and score.
- Used as the final context block for an LLM.

### `__main__` demo

```python
chunked_docs = load_and_chunk_corpus("data/corpus.json", chunk_size=40)
collection = build_chroma_collection(chunked_docs, ...)
iteration_results = iterative_retrieval("What internal policies apply specifically to employees?", collection)
final_context = build_final_context(iteration_results)
```

It loads a tiny JSON corpus, builds a Chroma collection (embedding happens inside `build_chroma_collection`), runs the iterative process, and prints the evolving queries + final context.

---

**Summary of the whole system**

You now have:

- A clear conceptual explanation of **iterative retrieval**
- A ready-to-use **README.md** that documents the technique and compares it to other RAG methods
- A line-by-line understanding of the **production-ready Python implementation**

The code is deliberately simple, dependency-light, and easy to plug into any existing Chroma + RAG pipeline. You can swap the keyword extractor for an LLM rewriter later without changing the overall iterative loop structure. Enjoy building more accurate RAG systems!
