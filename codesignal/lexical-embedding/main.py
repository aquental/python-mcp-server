from rank_bm25 import BM25Okapi
from data import load_and_chunk_corpus
from vector_db import build_chroma_collection


def build_bm25_index(chunks):
    """
    Build a BM25Okapi index from the chunk texts for lexical-based retrieval.
    Note BM25 scores often range roughly between 0 and 10 (depending on corpus).
    """
    corpus = [c["text"].lower().split() for c in chunks]
    return BM25Okapi(corpus)


def hybrid_retrieval(query, chunks, bm25, collection, top_k=3, alpha=0.5):
    """
    Merge BM25 and embedding-based results.
    Steps:
      1) Compute BM25 scores for each chunk. (Higher = better)
      2) Get embedding distances from ChromaDB for a candidate set.
      3) Convert distances to similarity (e.g., similarity ~ 1/(1+distance)).
      4) Normalize both BM25 and similarity to [0,1] and combine with weighting:
         final_score = alpha * BM25_normalized + (1 - alpha) * embedding_similarity
      5) Discard any chunk with final_score < 0.2
      6) Sort remaining chunks by final score in descending order.
      7) Return the top_k results.

    'alpha' controls how much weight lexical vs. embedding-based similarity gets.
    """
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_min, bm25_max = (min(bm25_scores), max(bm25_scores)) if bm25_scores.size > 0 else (0, 1)

    embed_results = collection.query(query_texts=[query], n_results=min(top_k * 5, len(chunks)))
    embed_scores_dict = {}
    for i in range(len(embed_results['documents'][0])):
        idx = embed_results['ids'][0][i]
        distance = embed_results['distances'][0][i]
        similarity = 1 / (1 + distance)
        embed_scores_dict[idx] = similarity

    merged = []
    for i, chunk in enumerate(chunks):
        bm25_raw = bm25_scores[i]
        if bm25_max != bm25_min:
            bm25_norm = (bm25_raw - bm25_min) / (bm25_max - bm25_min)
        else:
            bm25_norm = 0.0

        embed_sim = embed_scores_dict.get(i, 0.0)
        final_score = alpha * bm25_norm + (1 - alpha) * embed_sim
        merged.append((i, final_score))

    # TODO: Filter out chunks with scores below 0.2 before sorting and selecting top_k results
    merged = [item for item in merged if item[1] >= 0.2]
    merged.sort(key=lambda x: x[1], reverse=True)
    top_results = merged[:top_k]

    print(f"Top results by combined BM25 + embeddings for query: '{query}'")
    for idx, score in top_results:
        print(f"Chunk: '{chunks[idx]['text'][:50]}...' | Score: {score:.4f}")
    return [(idx, chunks[idx], score) for (idx, score) in top_results]


if __name__ == "__main__":
    chunked_docs = load_and_chunk_corpus("data/corpus.json", 40)
    bm25_index = build_bm25_index(chunked_docs)
    collection = build_chroma_collection(chunked_docs, collection_name="hybrid_collection")

    query = "What do our internal company policies state?"
    results = hybrid_retrieval(query, chunked_docs, bm25_index, collection, top_k=3, alpha=0.6)
    if not results:
        print("No chunks found. Fallback to a naive or apology answer.")
    else:
        for r in results:
            chunk_idx, chunk_data, final_score = r
            print(f"Chunk ID: {chunk_idx}, Score: {final_score:.4f}, Text: {chunk_data['text']}")
