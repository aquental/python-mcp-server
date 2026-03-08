import re
from data import load_and_chunk_corpus
from vector_db import build_chroma_collection

# Optional: set this to 0.0 if you don't need to enforce a minimum improvement.
IMPROVEMENT_THRESHOLD = 0.02

# Common stopwords to ignore when extracting keywords
STOPWORDS = set([
    "the", "and", "is", "in", "of", "to", "a", "that", "for", "on", "with", "as", "it", "by",
    "this", "are", "was", "at", "from", "or", "be", "which", "not", "can", "also", "have",
    "has", "had", "we", "they", "you", "he", "she", "his", "her", "its", "our", "us", "their",
    "them", "i", "do", "does", "did", "just", "so", "if", "may", "will", "shall", "more", "most",
    "some", "many", "any", "all", "what", "about", "would", "could", "should", "where", "when",
    "why", "how"
])


def retrieve_best_chunk(query_text, collection, n_results=1):
    """
    Retrieve the best matching chunk from the collection based on the given query.
    Returns:
      best_chunk_text, best_chunk_score, best_chunk_metadata
      (or None, None, None if retrieval fails)
    """
    retrieval = collection.query(query_texts=[query_text], n_results=n_results)
    if not retrieval['documents'][0]:
        return None, None, None

    best_chunk_text = retrieval['documents'][0][0]
    best_distance = retrieval['distances'][0][0]
    best_chunk_score = 1 / (1 + best_distance)  # Simple inverted distance
    best_chunk_metadata = retrieval['metadatas'][0][0]
    return best_chunk_text, best_chunk_score, best_chunk_metadata


def extract_refinement_keywords(chunk_text, current_query, max_keywords=2):
    """
    Extract up to `max_keywords` new keywords from the chunk that are not already
    in the current query.
    - Ignores stopwords and short words (< 5 chars).
    - Returns unique candidates sorted by length (longest first).
    - If fewer than `max_keywords` are available, returns all of them.
    - If none are found, returns an empty list.
    """
    chunk_words = re.findall(r'\b\w+\b', chunk_text.lower())
    query_words = set(re.findall(r'\b\w+\b', current_query.lower()))

    candidate_words = [
        w for w in chunk_words
        if w not in STOPWORDS and w not in query_words and len(w) > 4
    ]

    if not candidate_words:
        return []

    # Unique candidates, sorted longest → shortest, take up to max_keywords
    unique_candidates = sorted(set(candidate_words), key=len, reverse=True)
    return unique_candidates[:max_keywords]


def refine_query(current_query, refine_word):
    """
    Append the chosen refine_word to the current query if it exists.
    """
    if not refine_word:
        return current_query
    return f"{current_query} {refine_word}"


def iterative_retrieval(query, collection, steps=3):
    """
    Multi-step retrieval with a simple query refinement approach:
      1) Retrieve the best chunk for the current query.
      2) Extract up to TWO new keywords from that chunk and append them.
      3) Stop if no improvement in similarity or no new keywords are found.
      4) Collect the chunks from each step for final context.

    This version uses a global IMPROVEMENT_THRESHOLD to decide if we should keep refining.
    """
    accumulated_chunks = []
    current_query = query
    best_score_so_far = 0.0

    for step in range(steps):
        print(f"Iteration {step+1}, current query: '{current_query}'")

        best_chunk_text, best_chunk_score, best_chunk_metadata = retrieve_best_chunk(
            current_query, collection)
        if not best_chunk_text:
            print("No chunks found at this step. Ending refinement.")
            break

        print(
            f"Best chunk text (first 50 chars): '{best_chunk_text[:50]}...' | Score: {best_chunk_score:.4f}")

        if best_chunk_score - best_score_so_far < IMPROVEMENT_THRESHOLD:
            print("Improvement threshold not met. Stopping refinements.")
            break

        best_score_so_far = best_chunk_score

        accumulated_chunks.append({
            'step': step + 1,
            'query': current_query,
            'retrieved_chunk': {
                'text': best_chunk_text,
                'metadata': best_chunk_metadata
            },
            'score': best_chunk_score
        })

        # === UPDATED: extract up to 2 keywords and append each one ===
        keywords = extract_refinement_keywords(
            best_chunk_text, current_query, max_keywords=2)
        if not keywords:
            print("No suitable keyword found for further refinement.")
            break

        for refine_word in keywords:
            print(f"Refining query with keyword: {refine_word}")
            current_query = refine_query(current_query, refine_word)

    return accumulated_chunks


def build_final_context(iteration_results):
    """
    Combine all retrieved chunks from each iteration into one context block.
    Return a fallback message if no chunks were retrieved.
    """
    if not iteration_results:
        return "No relevant information was found after iterative retrieval."

    lines = []
    for result in iteration_results:
        lines.append(
            f"- Step {result['step']} (Score={result['score']:.4f}): {result['retrieved_chunk']['text']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    # Small demonstration with a sample corpus
    chunked_docs = load_and_chunk_corpus("data/corpus.json", chunk_size=40)
    collection = build_chroma_collection(
        chunked_docs, collection_name="iterative_collection")

    initial_query = "What internal policies apply specifically to employees?"
    iteration_results = iterative_retrieval(initial_query, collection, steps=3)

    final_context = build_final_context(iteration_results)
    print(f"\nFinal combined context:\n{final_context}")
