from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions


def build_chroma_collection(chunks, collection_name="corpus_collection"):
    """
    Builds or retrieves a ChromaDB collection, embedding each chunk using a SentenceTransformer.
    Adds all chunks in the 'chunks' list to the collection for fast retrieval.
    """
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    client = Client(Settings())
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embed_func)

    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{c['doc_id']}_{c['chunk_id']}" for c in chunks]
    metadatas = [{"doc_id": c["doc_id"], "chunk_id": c["chunk_id"], "category": c["category"]} for c in chunks]

    # Add documents to the collection
    collection.add(documents=texts, metadatas=metadatas, ids=ids)

    return collection
