import pinecone
import os
from dotenv import load_dotenv

class PineconeVectorStore:
    """
    A class to interact with a Pinecone vector store.

    Args:
        index_name (str): The name of the Pinecone index.
    """

    def __init__(self, index_name: str):
        # Load environment variables
        load_dotenv()
        pinecone_api_key = os.getenv("9312d1f7-9586-4d57-a033-3590ae384fde")
        pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")

        if not pinecone_api_key or not pinecone_environment:
            raise ValueError("Pinecone API key or environment not set in .env file.")

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

        # Create or connect to the index
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=384, metric="cosine")  # Adjust metric as needed
        self.index = pinecone.Index(index_name)

    def add_embeddings(self, ids: list[str], embeddings: list[list[float]]):
        """
        Adds embeddings to the Pinecone index.

        Args:
            ids (list[str]): A list of IDs for the embeddings.
            embeddings (list[list[float]]): A list of embedding vectors.
        """

        vectors = [{"id": id_, "vector": embedding} for id_, embedding in zip(ids, embeddings)]
        self.index.upsert(vectors=vectors)

    def search(self, query_vector: list[float], top_k: int = 5) -> list:
        """
        Searches the index for the top-k nearest neighbors to the query vector.

        Args:
            query_vector (list[float]): The query vector.
            top_k (int, optional): The number of nearest neighbors to return. Defaults to 5.

        Returns:
            list: A list of tuples, where each tuple contains the ID, score, and metadata of a nearest neighbor.
        """

        query_results = self.index.query(vector=query_vector, top_k=top_k)
        return query_results["matches"]
