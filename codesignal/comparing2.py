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


def build_vocab(docs):
    """
    Dynamically build a vocabulary from the given docs.
    Each new word or bigram in the corpus is an entry in the vocabulary.
    """
    unique_tokens = set()
    for doc in docs:
        words = [word.strip(".,!?") for word in doc.lower().split()]
        # Add unigrams
        for i in range(len(words)):
            if words[i]:
                unique_tokens.add(words[i])
        # Add bigrams (pairs of consecutive words)
        for i in range(len(words) - 1):
            if words[i] and words[i + 1]:
                bigram = f"{words[i]} {words[i + 1]}"
                unique_tokens.add(bigram)
    return {token: idx for idx, token in enumerate(sorted(unique_tokens))}


VOCAB = build_vocab(KNOWLEDGE_BASE)


def bow_vectorize(text, vocab=VOCAB):
    """
    Convert a text into a Bag-of-Words vector, using a shared vocabulary.
    Each element counts how many times a particular token or bigram appears.
    """
    vector = np.zeros(len(vocab), dtype=int)
    words = [word.strip(".,!?") for word in text.lower().split()]
    # Count unigrams
    for i in range(len(words)):
        if words[i] and words[i] in vocab:
            vector[vocab[words[i]]] += 1
    # Count bigrams (pairs of consecutive words)
    for i in range(len(words) - 1):
        if words[i] and words[i + 1]:
            bigram = f"{words[i]} {words[i + 1]}"
            if bigram in vocab:
                vector[vocab[bigram]] += 1
    return vector


def bow_search(query, docs):
    """
    Rank documents by lexical overlap (BOW) using unigrams and bigrams.
    The dot product between query and doc vectors reflects how many
    tokens they have in common.
    """
    query_vec = bow_vectorize(query)
    scores = []
    for i, doc in enumerate(docs):
        doc_vec = bow_vectorize(doc)
        score = np.dot(query_vec, doc_vec)
        scores.append((i, score))
    # Sort documents so that higher lexical overlap is first
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


if __name__ == "__main__":
    query = "How does a system combine external data with language generation to improve responses?"
    print(f"Query: {query}")

    print(f"Vocabulary: {VOCAB}")

    # BOW-based search
    bow_results = bow_search(query, KNOWLEDGE_BASE)
    print("BOW Search Results:")
    for idx, score in bow_results:
        print(f"  Doc {idx} | Score: {score} | Text: {KNOWLEDGE_BASE[idx]}")
