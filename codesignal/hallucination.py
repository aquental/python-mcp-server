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


def rag_retrieval(query, knowledge_base, k=2):
    # Convert the query to lowercase and tokenize into words
    query_lower = query.lower()
    query_tokens = set(query_lower.split())

    # List to store (overlap_score, doc_key, doc_dict) tuples
    scored_docs = []

    print("Overlap scores:")
    print("-" * 40)

    # Score each document
    for doc_key, doc in knowledge_base.items():
        # Convert document content to lowercase and tokenize
        content_lower = doc["content"].lower()
        doc_tokens = set(content_lower.split())

        # Calculate overlap (number of shared words)
        overlap = len(query_tokens.intersection(doc_tokens))

        # Store the result
        scored_docs.append((overlap, doc_key, doc))

        # Print for visibility
        print(f"{doc_key:6s} | overlap = {overlap:2d} words")

    print("-" * 40)

    # Sort by overlap score descending, then take top k
    # sorts by first element (overlap) descending
    scored_docs.sort(reverse=True)

    # Extract just the document dictionaries (top k)
    top_documents = [doc for _, _, doc in scored_docs[:k]]

    return top_documents


def rag_generation(query, documents):
    if documents:
        snippet = ""
        for doc in documents:
            snippet += f"{doc['title']}:\n{doc['content']}\n\n"
        prompt = (
            "Use ONLY the information provided below to answer the query. "
            "Be factual and include numbers exactly as they appear.\n\n"
            f"Provided information:\n{snippet}\n"
            f"Query: {query}\n\n"
            "Answer:"
        )
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

    print("=== Naive approach ===")
    print(naive_generation(query))
    print("\n")

    print("=== RAG retrieval debug ===")
    top_docs = rag_retrieval(query, KNOWLEDGE_BASE, k=2)

    print(f"\nRetrieved {len(top_docs)} document(s)")

    print("\n=== RAG approach ===")
    print(rag_generation(query, top_docs))
