import faiss
import numpy as np

class LocalVectorStore:
    """
    Stores and searches for vector embeddings in memory using FAISS.

    Attributes:
        index (faiss.IndexFlatL2): The FAISS index for efficient search.
        embeddings (list): A list of stored embeddings.
    """

    def __init__(self, embedding_dim: int):
        """
        Initializes the vector store with the specified embedding dimension.

        Args:
            embedding_dim (int): The dimension (length) of each embedding vector.
        """

        self.index = faiss.IndexFlatL2(embedding_dim)
        self.embeddings = []

    def add_embeddings(self, embeddings: list):
        """
        Adds a list of embeddings to the store and updates the index.

        Args:
            embeddings (list): A list of embedding vectors.
        """

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.embeddings.extend(embeddings)  # Efficiently extend the list

    def search(self, query_vector: list, top_k: int = 5) -> list:
        """
        Searches for nearest neighbors to a query vector.

        Args:
            query_vector (list): The query vector to search with.
            top_k (int, optional): The number of nearest neighbors to return. Defaults to 5.

        Returns:
            list: A list containing two elements:
                - Distances: A list of distances to the nearest neighbors.
                - Indices: A list of indices of the nearest neighbors in the self.embeddings list.
        """

        query = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query, top_k)
        return [distances.tolist()[0], indices.tolist()[0]]  # Convert to single-element lists