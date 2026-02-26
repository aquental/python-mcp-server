from scripts.llm import get_llm_response

KNOWLEDGE_BASE = {
    "doc1": {
        "title": "Project Chimera Overview",
        "content": (
            "Project Chimera is a research initiative focused on developing "
            "novel bio-integrated interfaces. It aims to merge biological "
            "systems with advanced computing technologies."
        )
    },
    "doc2": {
        "title": "Chimera's Neural Interface",
        "content": (
            "The core component of Project Chimera is a neural interface "
            "that allows for bidirectional communication between the brain "
            "and external devices. This interface uses biocompatible "
            "nanomaterials."
        )
    },
    "doc3": {
        "title": "Applications of Chimera",
        "content": (
            "Potential applications of Project Chimera include advanced "
            "prosthetics, treatment of neurological disorders, and enhanced "
            "human-computer interaction. Ethical considerations are paramount."
        )
    }
}

# TODO: Implement the naive_generation function
# Parameters:
#   query (str): The user's question
# Returns:
#   str: Direct response from LLM without context
# Function should create a simple prompt and return LLM's response


def naive_generation(query: str) -> str:
    """
    Generate answer without using any context from the knowledge base.
    """
    prompt = f"Answer the following question directly:\n{query}"
    return get_llm_response(prompt)

# TODO: Implement the rag_retrieval function
# Parameters:
#   query (str): The user's question
#   documents (dict): The knowledge base
# Returns:
#   dict: The most relevant document based on keyword overlap
# Steps:
# 1. Convert query to lowercase words set
# 2. For each document, calculate word overlap
# 3. Return document with highest overlap


def rag_retrieval(query: str, documents: dict) -> dict | None:
    """
    Find the document with the highest keyword overlap with the query.

    Returns:
        The most relevant document dict, or None if no overlap found.
    """
    if not query.strip():
        return None

    query_words = set(query.lower().split())
    best_doc = None
    best_overlap = -1

    for doc_id, doc in documents.items():
        # Using content only (you could also include title if desired)
        doc_words = set(doc["content"].lower().split())
        overlap_count = len(query_words.intersection(doc_words))

        if overlap_count > best_overlap:
            best_overlap = overlap_count
            best_doc = doc

    # Only return document if there was at least some overlap
    return best_doc if best_overlap > 0 else None

# TODO: Implement the rag_generation function
# Parameters:
#   query (str): The user's question
#   document (dict): The retrieved document
# Returns:
#   str: Context-aware response from LLM
# Steps:
# 1. If document exists, create prompt with document content
# 2. If no document, create direct prompt
# 3. Return LLM's response


def rag_generation(query: str, document: dict | None) -> str:
    """
    Generate answer using the retrieved document as context (if available).
    """
    if document:
        context = f"{document['title']}\n{document['content']}"
        prompt = (
            "Answer the question based ONLY on the following context. "
            "Do not add information that is not present in the context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )
    else:
        prompt = (
            "No relevant information was found in the knowledge base. "
            f"Please answer the following question to the best of your ability:\n"
            f"{query}"
        )

    return get_llm_response(prompt)


if __name__ == "__main__":
    query = "What is the main goal of Project Chimera?"

    print("=== Naive Generation (no context) ===")
    naive_answer = naive_generation(query)
    print(naive_answer)
    print()

    print("=== RAG Approach ===")
    retrieved_doc = rag_retrieval(query, KNOWLEDGE_BASE)

    if retrieved_doc:
        print("Retrieved document:", retrieved_doc["title"])
        print("-" * 50)
    else:
        print("No relevant document found.")
        print("-" * 50)

    rag_answer = rag_generation(query, retrieved_doc)
    print(rag_answer)
