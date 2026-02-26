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
    query_words = set(query.lower().split())
    best_doc_id = None
    best_overlap = 0
    for doc_id, doc in knowledge_base.items():
        doc_words = set(doc["content"].lower().split())
        overlap = len(query_words.intersection(doc_words))
        if overlap > best_overlap:
            best_overlap = overlap
            best_doc_id = doc_id
    return knowledge_base.get(best_doc_id)


def rag_generation(query, document):
    if not document:
        prompt = (
            f"The query asks for specific stock data, but no relevant document was found in the knowledge base.\n"
            f"Query: {query}\n\n"
            "Do NOT attempt to answer or guess. Respond only with:\n"
            "I'm sorry, but I don't have any information about the requested stock(s) in my knowledge base."
        )
    else:
        context = f"{document['title']}:\n{document['content']}"
        prompt = f"""You are a precise financial data assistant with access ONLY to the following document:

{context}

User query:
{query}

Instructions - follow these rules strictly in order:

1. The query asks for April 14, 2023 opening price, closing price, high, low, and trading volume for one or more specific stock symbols.
2. Check carefully whether this SINGLE document contains COMPLETE and EXACT data for EVERY symbol requested in the query, specifically for the date April 14, 2023.
3. If the document:
   - contains data for ALL requested symbols
   - AND includes ALL required fields (open, close, high, low, volume) for April 14, 2023
   → then provide a concise, factual summary using ONLY numbers from the document.
4. If ANY of the following is true:
   - The document is about a different symbol than requested
   - Data for April 14, 2023 is missing for any requested symbol
   - Any required field (open, close, high, low, volume) is missing
   - The query asks for multiple symbols but this document covers only one
   → then DO NOT answer the question. Instead respond ONLY with:

   "I'm sorry, but the available information does not contain complete data for all the requested symbols and date. I cannot provide an accurate answer based on the current knowledge base."

5. Never use knowledge outside this document. Never guess or infer missing values.

Your response:"""

    return get_llm_response(prompt)


if __name__ == "__main__":
    query = (
        "Write a short summary of the stock market performance on April 14, "
        "2023 for the following symbols: NVDA, GOOG.\n"
        "Your summary should include:\n"
        "For each symbol:\n"
        "- The opening price\n"
        "- The closing price\n"
        "- The highest and lowest prices of the day\n"
        "- The trading volume"
    )
    print("Naive approach:\n", naive_generation(query))
    retrieved_doc = rag_retrieval(query, KNOWLEDGE_BASE)
    print("\n\nRAG approach:\n", rag_generation(query, retrieved_doc))
