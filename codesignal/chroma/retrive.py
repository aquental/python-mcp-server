import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from scripts.llm import get_llm_response


def retrieve_top_chunks(query, collection, category=None, top_k=3, distance_threshold=1.0):
    """
    Retrieves the top_k chunks most relevant to the given query from 'collection',
    optionally filtered by category, and only includes those whose distance is
    below the specified distance_threshold. Returns a list of retrieved chunks,
    each containing 'chunk', 'doc_id', and 'distance'.
    
    Note: distance_threshold=1.0 is a carefully chosen cutoff for this embedding model
    (all-MiniLM-L6-v2 with Chroma's default squared L2 space). It corresponds to
    cosine similarity > ~0.5 — a good balance between relevance and recall.
    """
    where = {"category": category} if category is not None else None

    results = collection.query(
        query_texts=[query],
        where=where,
        n_results=top_k
    )

    retrieved_chunks = []
    if not results["documents"] or not results["documents"][0]:
        return retrieved_chunks

    # Process the results and apply distance-based filtering
    # Both the category (metadata) filter and distance threshold are now applied together
    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]
        if distance < distance_threshold:
            chunk_info = {
                "chunk": results["documents"][0][i],
                "doc_id": results["ids"][0][i],
                "distance": distance
            }
            retrieved_chunks.append(chunk_info)

    return retrieved_chunks


def build_prompt(query, retrieved_chunks):
    """
    Constructs a prompt by combining the query and retrieved chunks into a
    context block, guiding the LLM to provide a context-based answer.
    """
    prompt = f"Question: {query}\nAnswer using only the following context:\n"
    for rc in retrieved_chunks:
        prompt += f"- {rc['chunk']}\n"
    prompt += "Answer:"
    return prompt


if __name__ == "__main__":
    # Load corpus data from JSON file
    with open("data/corpus.json", "r") as f:
        corpus_data = json.load(f)

    # Prepare documents, ids, and metadatas
    documents = [doc["content"] for doc in corpus_data]
    ids = [f"chunk_{doc['id']}_0" for doc in corpus_data]
    metadatas = [{"category": doc.get("category", "")} for doc in corpus_data]

    # Create or retrieve the vector database collection
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    client = Client(Settings())
    collection = client.get_or_create_collection("rag_collection", embedding_function=embed_func)

    # Add documents with metadata to the collection
    collection.add(documents=documents, ids=ids, metadatas=metadatas)

    # Define query parameters (query string, category, and distance threshold)
    user_query = "What are the latest AI breakthroughs?"  # Example query
    user_category = "Technology"
    threshold = 1.0

    # Retrieve and filter chunks
    filtered_chunks = retrieve_top_chunks(
        query=user_query,
        collection=collection,
        category=user_category,
        top_k=5,
        distance_threshold=threshold
    )

    # TODO: Handle the filtered chunks:
    # - If no chunks found, print a user-friendly message
    # - Otherwise, build the prompt and get LLM response
    if not filtered_chunks:
        print("😕 No relevant chunks found matching your query and category.")
        print("   No documents met the similarity threshold (distance < 1.0).")
        print("   Try a broader category, remove the category filter, or increase the distance_threshold.")
    else:
        prompt = build_prompt(user_query, filtered_chunks)
        print("=== Generated Prompt ===")
        print(prompt)
        print("\n=== LLM Response ===")
        answer = get_llm_response(prompt)
        print(answer)
