from scripts.llm import get_llm_response

KNOWLEDGE_BASE = {
    "AAPL": {
        "title": "AAPL Stock (April 2023)",
        "content": (
            "On 2023-04-13, AAPL opened at $160.50, closed at $162.30, with a high of $163.00 and a low of $159.90. "
            "Trading volume was 80 million shares. "
            "On 2023-04-14, AAPL opened at $161.10, closed at $162.80, with a high of $163.50 and a low of $160.50. "
            "Trading volume was 85 million shares."
        )
    },
    "MSFT": {
        "title": "MSFT Stock (April 2023)",
        "content": (
            "On 2023-04-13, MSFT opened at $285.00, closed at $288.50, with a high of $290.00 and a low of $283.50. "
            "Trading volume was 35 million shares. "
            "On 2023-04-14, MSFT opened at $286.00, closed at $289.00, with a high of $291.50 and a low of $284.70. "
            "Trading volume was 40 million shares."
        )
    },
    "TSLA": {
        "title": "TSLA Stock (April 2023)",
        "content": (
            "On 2023-04-13, TSLA opened at $185.00, closed at $187.00, with a high of $189.00 and a low of $184.50. "
            "Trading volume was 50 million shares. "
            "On 2023-04-14, TSLA opened at $186.00, closed at $188.50, with a high of $190.00 and a low of $185.50. "
            "Trading volume was 55 million shares."
        )
    }
}


def naive_generation(query):
    prompt = f"Answer directly the following query: {query}"
    return get_llm_response(prompt)


def rag_retrieval(query, knowledge_base):
    """
    Returns ALL documents that have at least one word in common with the query.
    This ensures we retrieve information for every mentioned stock symbol
    that appears in the knowledge base.
    """
    # Normalize query: lowercase and split into words
    query_lower = query.lower()
    query_words = set(query_lower.split())

    relevant_docs = []

    # Optional: show which documents are being selected (for debugging/visibility)
    print("RAG Retrieval - matched documents:")
    print("-" * 50)

    for key, doc in knowledge_base.items():
        # Normalize document content
        content_lower = doc["content"].lower()
        doc_words = set(content_lower.split())

        # If there's any overlap → consider the document relevant
        if query_words.intersection(doc_words):
            relevant_docs.append(doc)
            print(f"✓ {key:6s}  ({doc['title']})")
        else:
            print(f"  {key:6s}  (no overlap)")

    print("-" * 50)
    print(f"→ Returning {len(relevant_docs)} relevant document(s)\n")

    return relevant_docs


def rag_generation(query, documents):
    if documents:
        snippets = " ".join(
            [f"{doc['title']}: {doc['content']}" for doc in documents])
        prompt = f"Using the following information: '{snippets}', answer: {query}"
    else:
        prompt = f"No relevant information found. Answer directly: {query}"
    return get_llm_response(prompt)


if __name__ == "__main__":
    query = (
        "Write a short summary of the stock market performance on April 14, "
        "2023 for the following symbols: AAPL, MSFT, TSLA.\n"
        "Your summary should include:\n"
        "For each symbol:\n"
        "- The opening price\n"
        "- The closing price\n"
        "- The highest and lowest prices of the day\n"
        "- The trading volume"
    )
    # Naive approach hallucinates (generates a random plausible, but incorrect, answer)
    print("Naive approach:\n", naive_generation(query))
    # RAG approach prevents hallucination by "grounding" the answer (providing additional context)
    retrieved_docs = rag_retrieval(query, KNOWLEDGE_BASE)
    print("\n\nRAG approach:\n", rag_generation(query, retrieved_docs))
