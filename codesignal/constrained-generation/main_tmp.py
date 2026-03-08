__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from data import load_and_chunk_corpus
from vector_db import build_chroma_collection
from scripts.llm import get_llm_response

def generate_with_constraints(query, retrieved_context, strategy="base"):
    """
    Thoroughly enforce model reliance on 'retrieved_context' when answering 'query.'

    The 'strategy' parameter allows for different prompt template variations:
      1) Base approach: Provide context, instruct LLM not to use outside info, 
         and respond with 'No sufficient data' if the context is insufficient.
      2) Strict approach: Provide context with explicit disclaimers if the answer is not found.
      3) Citation approach: Provide context, then request the LLM to cite the relevant lines.

    Robust fallback:
      - If 'retrieved_context' is empty, respond with an apology or neutral statement.
      - Optionally log each stage for debugging or performance analysis.
    """
    # Provide a safe fallback if no context is retrieved
    if not retrieved_context.strip():
        return ("I'm sorry, but I couldn't find any relevant information.", "No context used.")

    # Choose a prompt template based on strategy
    if strategy == "base":
        # base prompt template to instruct the model to use the provided context
        prompt = (
            "Use the following context to answer the question in a concise manner.\n\n"
            f"Context:\n{retrieved_context}\n"
            f"Question: '{query}'\n"
            "Answer:"
        )
    elif strategy == "strict":
        # Strict approach: explicitly disallow info beyond the provided context
        prompt = (
            "You must ONLY use the context provided below. If you cannot find the answer in the context, say: 'No sufficient data'.\n"
            "Do not provide any information not found in the context.\n\n"
            f"Context:\n{retrieved_context}\n"
            f"Question: '{query}'\n"
            "Answer:"
        )
    elif strategy == "cite":
        # Citation approach: require references to lines used
        prompt = (
            "Answer strictly from the provided context, and list the lines you used as evidence with 'Cited lines:'.\n"
            "If the context does not contain the information, respond with: 'Not available in the retrieved texts.'\n\n"
            f"Provided context (label lines as needed):\n{retrieved_context}\n"
            f"Question: '{query}'\n"
            "Answer:"
        )

    # Print the prompt for debugging or inspection
    print(f"Prompt: \n {prompt}\n")

    # Make call to the LLM
    response = get_llm_response(prompt)

    # Attempt to parse out 'Cited lines:' if present
    segments = response.split("Cited lines:")
    if len(segments) == 2:
        answer_part, used_context_part = segments
        return answer_part.strip(), used_context_part.strip()
    else:
        # If the LLM didn't provide citations, treat the entire response as the answer
        return response.strip(), "No explicit lines cited."


if __name__ == "__main__":
    # Example usage demonstrating retrieval followed by constrained generation

    # 1. Load and chunk a corpus
    chunked_docs = load_and_chunk_corpus("data/corpus.json")

    # 2. Build a collection in a vector database
    collection = build_chroma_collection(chunked_docs, collection_name="corpus_collection")

    # 3. Run a sample query
    query = "Highlight the main policies that apply to employees."
    retrieval_results = collection.query(query_texts=[query], n_results=2)

    # 4. Construct the retrieved context from top matches
    if not retrieval_results['documents'][0]:
        retrieved_context = ""
    else:
        retrieved_context = "\n".join(["- " + doc_text for doc_text in retrieval_results['documents'][0]])

    # 5. Execute constrained generation function for demonstration
    for strategy in ("base", "strict", "cite"):
        answer, used_context = generate_with_constraints(query, retrieved_context, strategy=strategy)
        print(f"Strategy: {strategy}")
        print(f"Constrained generation answer:\n{answer}")
        print(f"Context or lines used: {used_context}\n")
