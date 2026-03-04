import os
import json
import re


def chunk_text(text, chunk_size=30):
    """
    Splits the given text into chunks of size 'chunk_size', preserving sentence boundaries.
    Returns a list of chunk strings.
    """
    # Split text into sentences using regex
    # Hint: Use re.split() with appropriate punctuation marks
    # We use a capturing group ([.!?]+) so the punctuation stays attached to each sentence
    parts = re.split(r'([.!?]+)', text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        if i + 1 < len(parts):
            sent = (parts[i] + parts[i + 1]).strip()
            if sent:
                sentences.append(sent)
    # Handle possible trailing text without punctuation
    if len(parts) % 2 == 1 and parts[-1].strip():
        sentences.append(parts[-1].strip())

    # Process sentences into chunks while respecting chunk_size
    # Hint: Keep track of word count and create new chunks when needed
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        # Count words in this sentence (preserves the full sentence with its punctuation)
        sentence_words = sentence.split()
        sent_word_count = len(sentence_words)

        # If adding this full sentence would exceed the limit, save the current chunk first
        if current_word_count + sent_word_count > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0

        # Add the whole sentence to the current chunk
        current_chunk.append(sentence)
        current_word_count += sent_word_count

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def load_and_chunk_dataset(file_path, chunk_size=30):
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


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", "corpus.json")
    chunked_docs = load_and_chunk_dataset(dataset_file, chunk_size=30)
    print("Loaded and chunked", len(chunked_docs), "chunks from dataset.")
    for c in chunked_docs[:5]:          # show only first 5 for brevity
        print(c)
    print("... (and", len(chunked_docs) - 5, "more chunks)")
