from scripts.llm import get_llm_response

KNOWLEDGE_BASE = {
    "doc1": {
        "title": "Project Chimera Overview",
        "content": (
            "research initiative focused on developing novel bio-integrated "
            "interfaces, aiming at merging biological systems with advanced "
            "computing technologies."
        )
    },
    "doc2": {
        "title": "Chimera's Core Component",
        "content": (
            "a neural interface that allows for bidirectional communication "
            "between the brain and external devices, using biocompatible "
            "nanomaterials."
        )
    },
    "doc3": {
        "title": "Applications of Chimera",
        "content": (
            "advanced prosthetics, treatment of neurological disorders, "
            "enhanced human-computer interaction."
        )
    }
}


def naive_generation(query):
    prompt = f"Answer directly the following query: {query}"
    return get_llm_response(prompt)


def rag_retrieval(query, documents):
    query_words = set(query.lower().split())
    best_doc_id = None
    best_score = -1

    for doc_id, doc in documents.items():
        # TODO: Fix the bug by considering both title and content
        # Currently only looking at content, ignoring potentially relevant titles
        text = (doc["title"] + " " + doc["content"]).lower()
        doc_words = set(text.split())
        score = len(query_words.intersection(doc_words))

        if score > best_score:
            best_score = score
            best_doc_id = doc_id

    return documents.get(best_doc_id)


def rag_generation(query, document):
    if document:
        snippet = f"{document['title']}: {document['content']}"
        prompt = f"Using the following information: '{snippet}', answer: {query}"
    else:
        prompt = f"No relevant information found. Answer directly: {query}"
    return get_llm_response(prompt)


if __name__ == "__main__":
    query = "What are the applications of Project Chimera?"
    print("Naive approach:", naive_generation(query))
    retrieved_doc = rag_retrieval(query, KNOWLEDGE_BASE)
    print("RAG approach:", rag_generation(query, retrieved_doc))
