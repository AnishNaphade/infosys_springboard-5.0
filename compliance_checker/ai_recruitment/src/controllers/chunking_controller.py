def chunk_text(text, chunk_size=500, overlap=50):
    """
    Chunks a given text into smaller segments with an optional overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int, optional): The desired size of each chunk. Defaults to 500.
        overlap (int, optional): The number of characters to overlap between chunks. Defaults to 50.

    Returns:
        list: A list of text chunks.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks