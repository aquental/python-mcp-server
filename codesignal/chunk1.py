def chunk_text(text, chunk_size=10):
    """
    Splits the given text into chunks of size 'chunk_size'.
    Returns a list of chunk strings.
    """
    # TODO: Split the text into words
    words = text.split()  # Tokenize by splitting on whitespace
    # Construct chunks by stepping through the words list in increments of chunk_size
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


# Example text to test the chunking
sample_text = "This is a sample text that we will use to test our chunking function. It contains multiple sentences to make it more interesting."

# TODO: Call the chunk_text function with the sample text
chunked_list = chunk_text(sample_text, 6)
# TODO: Print each chunk on a new line to see how the text was split
for doc in chunked_list:
    print(doc)
