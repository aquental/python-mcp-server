import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions


def retrieve_top_chunks(query, collection, top_k=3):
    """
    Retrieves the top_k chunks most relevant to the given query from 'collection'.
    Returns a list of retrieved chunks, each containing 'chunk' text, 'doc_id', and 'distance'.
    """
    # Use collection.query() to search for documents matching the query
    # The query should return top_k results
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "distances"]  # Explicitly request what we need (ids always returned)
    )

    # Add safeguard for empty results
    if not results or not results.get("ids") or len(results["ids"][0]) == 0:
        print("No results found for the query.")
        return []

    # Process the results and append each chunk's information to retrieved_chunks
    # Each chunk should have: chunk text, doc_id, and distance score
    retrieved_chunks = []
    for i in range(len(results["ids"][0])):
        chunk_text = results["documents"][0][i]
        doc_id = results["ids"][0][i]
        distance = results["distances"][0][i]
        
        retrieved_chunks.append({
            "chunk": chunk_text,
            "doc_id": doc_id,
            "distance": distance
        })

    return retrieved_chunks


def build_prompt(query, retrieved_chunks):
    """
    Constructs an LLM prompt by combining multiple retrieved chunks into a
    single context block, ensuring the model can handle longer or more detailed answers.
    """
    prompt = f"Question: {query}\nAnswer using only the following context:\n"
    for rc in retrieved_chunks:
        prompt += f"- {rc['chunk']}\n"
    prompt += "Answer:"
    return prompt


if __name__ == "__main__":
    # Load a small set of documents from corpus.json
    with open('data/corpus.json', 'r') as f:
        corpus_data = json.load(f)

    # Set up the embedding function and create/get a ChromaDB collection
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    client = Client(Settings())
    collection = client.get_or_create_collection("rag_collection", embedding_function=embed_func)

    # Add documents from corpus_data to the collection
    documents = [doc['content'] for doc in corpus_data]
    ids = [f"chunk_{doc['id']}_0" for doc in corpus_data]
    collection.add(documents=documents, ids=ids)

    # Define a query string to test the retrieval function
    user_query = "technological breakthroughs"
    
    # Retrieve top matches
    retrieved_chunks = retrieve_top_chunks(user_query, collection, top_k=3)
    final_prompt = build_prompt(user_query, retrieved_chunks)
    llm_response = get_llm_response(final_prompt)

    # Print the retrieved chunks to verify the function's accuracy
    for rc in retrieved_chunks:
        print("Chunk:", rc["chunk"])
        print("Doc ID:", rc["doc_id"])
        print("Distance:", rc["distance"])
        print("-" * 40)
