import faiss
import numpy as np

def create_faiss_index(embeddings, metric='L2'):
    """
    Creates a FAISS index for efficient nearest neighbor search.

    Args:
        embeddings: A list of embeddings.
        metric: The distance metric to use ('L2' or 'cosine').

    Returns:
        A FAISS index object.
    """

    dimension = len(embeddings[0])
    if metric == 'L2':
        index = faiss.IndexFlatL2(dimension)
    elif metric == 'cosine':
        index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine similarity)
    else:
        raise ValueError("Invalid metric. Use 'L2' or 'cosine'.")

    index.add(np.array(embeddings).astype('float32'))
    return index

def save_faiss_index(index, path='data/vector_store/faiss.index'):
    """
    Saves a FAISS index to disk.

    Args:
        index: The FAISS index to save.
        path: The path to save the index.
    """

    faiss.write_index(index, path)

def load_faiss_index(path='data/vector_store/faiss.index'):
    """
    Loads a FAISS index from disk.

    Args:
        path: The path to the saved index.

    Returns:
        The loaded FAISS index.
    """

    return faiss.read_index(path)