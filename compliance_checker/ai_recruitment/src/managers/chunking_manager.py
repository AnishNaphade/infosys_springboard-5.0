def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits a given text into chunks of specified size with an optional overlap.

    Args:
        text: The input text to be chunked.
        chunk_size: The desired size of each chunk.
        overlap: The number of characters to overlap between chunks.

    Returns:
        A list of text chunks.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))  # Ensure end index doesn't exceed text length
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks