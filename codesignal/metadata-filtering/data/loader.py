import json


def chunk_text(text, chunk_size=50):
    """
    Splits the given text into chunks of size 'chunk_size'.
    Returns a list of chunk strings.
    """
    words = text.split()
    return [" ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size)]


def load_and_chunk_corpus(file_path, chunk_size=50):
    """
    Loads a dataset from JSON 'file_path', then splits each document into smaller chunks.
    Metadata such as 'doc_id' and 'category' is included with each chunk.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    all_chunks = []
    for doc_id, doc in enumerate(data):
        doc_text = doc["content"]
        doc_category = doc.get("category", "general")
        doc_chunks = chunk_text(doc_text, chunk_size)
        for chunk_id, chunk_str in enumerate(doc_chunks):
            all_chunks.append({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "category": doc_category,
                "text": chunk_str
            })
    return all_chunks
