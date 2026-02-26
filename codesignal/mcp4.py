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

def naive_generation(query):
    prompt = f"Answer directly the following query: {query}"
    return get_llm_response(prompt)


def rag_retrieval(query, documents):
    """
    Returns ALL documents that have at least one word in common with the query.
    """
    query_words = set(query.lower().split())
    
    relevant_docs = []
    
    for doc_id, doc in documents.items():
        doc_words = set(doc["content"].lower().split())
        overlap = query_words.intersection(doc_words)
        if overlap:  # if there's at least one common word
            relevant_docs.append(doc)
    
    return relevant_docs


def rag_generation(query, documents):
    """
    Handles a list of documents (can be empty).
    """
    if not documents:
        prompt = f"No relevant information found. Answer directly: {query}"
    else:
        # Build context from all relevant documents
        context_parts = []
        for doc in documents:
            snippet = f"{doc['title']}: {doc['content']}"
            context_parts.append(snippet)
        
        context = "\n\n".join(context_parts)
        
        prompt = (
            f"Use the following information to answer the question. "
            f"Only use information from the provided context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            f"Answer:"
        )
    
    return get_llm_response(prompt)


if __name__ == "__main__":
    query = "What are the applications of Project Chimera?"
    
    print("Naive approach:")
    print(naive_generation(query))
    print("\n" + "-"*60 + "\n")
    
    retrieved_docs = rag_retrieval(query, KNOWLEDGE_BASE)
    print(f"RAG approach (found {len(retrieved_docs)} document(s)):")
    print(rag_generation(query, retrieved_docs))
