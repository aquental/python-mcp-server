import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE = [
    "Retrieval-Augmented Generation (RAG) enhances language models by integrating relevant external documents into the generation process.",
    "RAG systems retrieve information from large databases to provide contextual answers beyond what is stored in the model.",
    "By merging retrieved text with generative models, RAG overcomes the limitations of static training data.",
    "Media companies combine external data feeds with digital editing tools to optimize broadcast schedules.",
    "Financial institutions analyze market data and use automated report generation to guide investment decisions.",
    "Healthcare analytics platforms integrate patient records with predictive models to generate personalized care plans.",
    "Bananas are popular fruits that are rich in essential nutrients such as potassium and vitamin C."
]


def cos_sim(a, b):
    """
    Calculate cosine similarity between two vectors.
    Formula: (A · B) / (|A| × |B|)
    """
    # TODOs completed:
    dot_product = np.dot(a, b)
    norm_a = norm(a)
    norm_b = norm(b)

    # Prevent division by zero (though SentenceTransformer embeddings are never zero)
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def embedding_search(query, docs, model):
    """
    Perform semantic search using sentence-transformer embeddings + cosine similarity.
    """
    # Encode the query into an embedding (shape: 384,)
    query_emb = model.encode(query)

    # Encode the documents into embeddings (shape: [n_docs, 384])
    doc_embs = model.encode(docs)

    # Calculate and store the cosine similarity between query_emb and each document embedding
    scores = []
    for i, doc_emb in enumerate(doc_embs):
        score = cos_sim(query_emb, doc_emb)
        scores.append((i, score))

    # Sort the scores in descending order of similarity
    scores.sort(key=lambda x: x[1], reverse=True)

    # Return list of (doc_index, similarity_score) tuples
    return scores


if __name__ == "__main__":
    query = "How does a system combine external data with language generation to improve responses?"
    print(f"Query: {query}")

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    emb_results = embedding_search(query, KNOWLEDGE_BASE, model)
    print("\nEmbedding-based Search Results:")
    for idx, score in emb_results:
        print(
            f"  Doc {idx} | Score: {score:.4f} | Text: {KNOWLEDGE_BASE[idx]}")
