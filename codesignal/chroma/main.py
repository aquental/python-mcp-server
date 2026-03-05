import os
import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions


def chunk_text(text, chunk_size=50):
    """
    Splits the given text into chunks of size 'chunk_size'.
    Returns a list of chunk strings.
    """
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


def load_and_chunk_dataset(file_path, chunk_size=50):
    """
    Loads a dataset from JSON 'file_path', then splits each document into smaller chunks.
    Metadata such as 'doc_id' and 'category' is included with each chunk.
    """
    # Open and load the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_chunks = []
    for doc in data:
        doc_text = doc["content"]
        # Extract category and id from the document
        doc_id = doc["id"]
        category = doc["category"]

        doc_chunks = chunk_text(doc_text, chunk_size)
        for chunk_index, chunk_str in enumerate(doc_chunks):
            # Create a dictionary for each chunk with doc_id, chunk_id, category and text
            chunk = {
                "doc_id": doc_id,
                "chunk_id": chunk_index,
                "category": category,
                "text": chunk_str
            }
            all_chunks.append(chunk)

    return all_chunks


def build_chroma_collection(chunks, collection_name="rag_collection"):
    """
    Builds or retrieves a ChromaDB collection, embedding each chunk using a SentenceTransformer.
    Adds all chunks in the 'chunks' list to the collection for fast retrieval.
    """
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name)

    client = Client(Settings())
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embed_func
    )

    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{c['doc_id']}_{c['chunk_id']}" for c in chunks]
    metadatas = [
        {"doc_id": c["doc_id"], "chunk_id": c["chunk_id"],
            "category": c["category"]}
        for c in chunks
    ]

    collection.add(documents=texts, metadatas=metadatas, ids=ids)
    return collection


def delete_documents_with_keyword(collection, keyword):
    """
    Deletes all documents from the given ChromaDB 'collection' whose text contains 'keyword'.
    """
    # Get all documents and their IDs from the collection
    results = collection.get()
    ids = results["ids"]
    documents = results["documents"]

    # Create a list to store IDs of documents containing the keyword
    ids_to_delete = []

    # Iterate through documents and their IDs, adding matching document IDs to the list
    for doc_id, doc_text in zip(ids, documents):
        if keyword.lower() in doc_text.lower():
            ids_to_delete.append(doc_id)

    # If there are documents to delete, remove them from the collection
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", "corpus.json")

    # Build the initial collection from chunked documents
    chunked_docs = load_and_chunk_dataset(dataset_file, chunk_size=30)
    collection = build_chroma_collection(chunked_docs)
    total_docs = collection.count()
    print("ChromaDB collection created with", total_docs, "documents.")

    # Create a new document dictionary with doc_id, chunk_id, category, and text
    # The text should be "Bananas are yellow fruits rich in potassium."
    new_document = {
        "doc_id": 999,
        "chunk_id": 0,
        "category": "nutrition",
        "text": "Bananas are yellow fruits rich in potassium."
    }

    # Generate a unique ID string for the new document
    new_doc_id = f"chunk_{new_document['doc_id']}_{new_document['chunk_id']}"

    # Add the new document to the collection using collection.add()
    # Don't forget to include the document text, metadata, and ID
    collection.add(
        documents=[new_document["text"]],
        metadatas=[{
            "doc_id": new_document["doc_id"],
            "chunk_id": new_document["chunk_id"],
            "category": new_document["category"]
        }],
        ids=[new_doc_id]
    )

    # Print the updated document count
    updated_count = collection.count()
    print("Updated document count after adding new document:", updated_count)

    # Remove the newly added document using collection.delete()
    collection.delete(ids=[new_doc_id])

    # Print the final document count
    final_count = collection.count()
    print("Final document count after deletion:", final_count)

    # Now delete all documents containing the keyword "Bananas".
    delete_documents_with_keyword(collection, "Bananas")

    # Print the final document count
    final_count = collection.count()
    print("Final document count after deletion:", final_count)
