from data import load_and_chunk_corpus
from vector_db import build_chroma_collection
from scripts.llm import get_llm_response

def are_chunks_overlapping(chunks, similarity_threshold=0.8):
    """
    Basic check for overlapping or highly similar chunk texts.
    In a production system, you'd compute embeddings for each chunk
    and measure pairwise similarity. Here, we simply check if chunks
    have large lexical overlap (placeholder approach).
    """
    if len(chunks) < 2:
        return False

    text_sets = [set(c["text"].split()) for c in chunks]
    for i in range(len(text_sets) - 1):
        for j in range(i + 1, len(text_sets)):
            overlap = len(text_sets[i].intersection(text_sets[j])) / max(len(text_sets[i]), 1)
            if overlap > similarity_threshold:
                return True
    return False

def summarize_chunks(chunks):
    """
    Combine multiple chunks into a single summary with an LLM.
    - If no chunks or user decides not to summarize, we skip.
    - If the summary is too short or drops essential info, we can fallback or retry.
    """
    if not chunks:
        return "No relevant chunks were retrieved."

    combined_text = "\n".join(c["text"] for c in chunks)
    prompt = (
        "You are an expert summarizer. Please generate a concise summary of the following text.\n"
        "Do not omit critical details that might answer the user's query.\n"
        "If you cannot produce a meaningful summary, just say 'Summary not possible'.\n\n"
        f"Text:\n{combined_text}\n\nSummary:"
    )

    summary = get_llm_response(prompt).strip()

    # === CORRECTED CHECK ===
    if len(summary) < 20 or "Summary not possible" in summary:
        print("Summary was too short or not possible. Providing full chunks instead.")
        return combined_text

    return summary

def final_generation(query, context):
    """
    Provide the final answer using either the summarized or plain context.
    If no context is available, fallback is triggered.
    """
    if not context.strip():
        return "I'm sorry, but I couldn't find any relevant information."

    prompt = (
        f"Question: {query}\n"
        f"Context:\n{context}\n"
        "Answer:"
    )
    return get_llm_response(prompt)

if __name__ == "__main__":
    chunked_docs = load_and_chunk_corpus("data/corpus.json", chunk_size=40)
    collection = build_chroma_collection(chunked_docs, "summary_demo_collection")

    user_query = "Provide an overview of our internal policies."
    retrieval_results = collection.query(query_texts=[user_query], n_results=5)

    if not retrieval_results['documents'][0]:
        print("No chunks were retrieved for the query.")
        final_answer = "No relevant information found."
    else:
        retrieved_chunks = []
        for doc_text in retrieval_results['documents'][0]:
            retrieved_chunks.append({"text": doc_text})

        # Decide whether to summarize based on the number or overlap of chunks
        if len(retrieved_chunks) > 3 or are_chunks_overlapping(retrieved_chunks):
            context = summarize_chunks(retrieved_chunks)
        else:
            context = "\n".join(f"- {c['text']}" for c in retrieved_chunks)

        final_answer = final_generation(user_query, context)

    print(f"Final answer:\n{final_answer}")
