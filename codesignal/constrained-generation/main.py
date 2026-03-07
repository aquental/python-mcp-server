from data import load_and_chunk_corpus
from vector_db import build_chroma_collection
from scripts.llm import get_llm_response

def generate_with_constraints(query, retrieved_context, strategy="base"):
    """
    Thoroughly enforce model reliance on 'retrieved_context' when answering 'query.'
    
    Now includes context-length validation and smart truncation if the context 
    exceeds a rough limit of 4096 tokens (approx. word-based).

    The 'strategy' parameter allows for different prompt template variations:
      1) Base approach: Provide context, instruct LLM not to use outside info.
      2) Strict approach: Provide context with explicit disclaimers if the answer is not found.
      3) Citation approach: Provide context, then request the LLM to cite the relevant lines.

    Robust fallback:
      - If 'retrieved_context' is empty, respond with an apology or neutral statement.
      - If 'retrieved_context' is too long, it is truncated while preserving whole sentences,
        and "[Context truncated]" is appended to the answer to warn the user.
    """
    # Provide a safe fallback if no context is retrieved
    if not retrieved_context.strip():
        return ("I'm sorry, but I couldn't find any relevant information.", "No context used.")

    # Define the maximum token limit for the context (rough word-based approximation)
    MAX_TOKENS = 4096

    # Implement context length validation and smart truncation
    # Check if context exceeds token limit and truncate while preserving whole sentences
    # Hint: Split into words first to check length, then into sentences for truncation
    words = retrieved_context.split()
    truncated = False

    if len(words) > MAX_TOKENS:
        truncated = True
        # Truncate to MAX_TOKENS words first (safe prefix)
        truncated_words = words[:MAX_TOKENS]
        truncated_str = ' '.join(truncated_words)
        
        # Smart backtracking: keep only complete sentences by finding the LAST
        # sentence-ending punctuation (., ! or ?) in the prefix. This guarantees
        # we never cut a sentence in the middle while staying under the limit.
        last_punct_pos = max(
            truncated_str.rfind('.'),
            truncated_str.rfind('!'),
            truncated_str.rfind('?')
        )
        if last_punct_pos != -1:
            retrieved_context = truncated_str[:last_punct_pos + 1].strip()
        else:
            # Extremely rare case: no punctuation at all in first 4096 words
            retrieved_context = truncated_str.strip()

    # Build the prompt based on strategy (now using the possibly truncated context)
    if strategy == "base":
        prompt = (
            "Use the following context to answer the question in a concise manner.\n\n"
            f"Context:\n{retrieved_context}\n"
            f"Question: '{query}'\n"
            "Answer:"
        )
    elif strategy == "strict":
        prompt = (
            "You must ONLY use the context provided below. If you cannot find the answer in the context, say: 'No sufficient data'.\n"
            "Do not provide any information not found in the context.\n\n"
            f"Context:\n{retrieved_context}\n"
            f"Question: '{query}'\n"
            "Answer:"
        )
    elif strategy == "cite":
        prompt = (
            "Answer strictly from the provided context, and list the lines you used as evidence with 'Cited lines:'.\n"
            "If the context does not contain the information, respond with: 'Not available in the retrieved texts.'\n\n"
            f"Provided context (label lines as needed):\n{retrieved_context}\n"
            f"Question: '{query}'\n"
            "Answer:"
        )

    print(f"Prompt: \n {prompt}\n")

    # Query the language model
    response = get_llm_response(prompt)

    # Attempt to parse out 'Cited lines:' if present
    segments = response.split("Cited lines:")
    if len(segments) == 2:
        answer_part, used_context_part = segments
        final_answer = answer_part.strip()
        cited_part = used_context_part.strip()
    else:
        final_answer = response.strip()
        cited_part = "No explicit lines cited."

    # Add truncation warning to the answer if context was truncated
    if truncated:
        final_answer += " [Context truncated]"

    return final_answer, cited_part


if __name__ == "__main__":
    # Demonstration of retrieval and constrained generation
    chunked_docs = load_and_chunk_corpus("data/corpus.json")
    collection = build_chroma_collection(chunked_docs, collection_name="corpus_collection")

    # Example query that might yield relevant or no results
    query = "Highlight the main policies that apply to employees."
    retrieval_results = collection.query(query_texts=[query], n_results=2)

    if not retrieval_results['documents'][0]:
        retrieved_context = ""
    else:
        retrieved_context = "\n".join(["- " + doc_text for doc_text in retrieval_results['documents'][0]])

    for strategy_option in ("base", "strict", "cite"):
        answer, used_context = generate_with_constraints(query, retrieved_context, strategy=strategy_option)
        print(f"Strategy: {strategy_option}")
        print(f"Constrained generation answer:\n{answer}")
        print(f"Context or lines used:\n{used_context}\n")
