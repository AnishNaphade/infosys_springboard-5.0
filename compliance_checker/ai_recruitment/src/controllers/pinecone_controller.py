import os
from pinecone import Pinecone, Index, ServerlessSpec

# Load Pinecone API key from environment variables
PINECONE_API_KEY = os.getenv("pcsk_72SfXg_DRq7pthSRqALXrKNPVx2pZRwBfrUdsEsxzX1UVKSF8kRihGsHCfBkaY2zMLXzoi")

# Initialize the Pinecone client
pc = Pinecone()
pc.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp")

def upsert_to_pinecone(index_name, embeddings, ids):
    """
    Upserts vectors to a Pinecone index.

    Args:
        index_name (str): The name of the Pinecone index.
        embeddings (list): A list of embeddings.
        ids (list): A list of IDs corresponding to the embeddings.

    Returns:
        dict: A dictionary indicating success or failure.
    """

    try:
        # Check if the index exists
        if index_name not in pc.list_indexes().names():
            # Create the index
            pc.create_index(
                name=index_name,
                dimension=len(embeddings[0]),
                metric="euclidean",  # Adjust metric as needed (e.g., cosine)
                metadata_config={
                    "indexed": ["text_field"]  # Add metadata fields to filter and query
                },
                pod_type="p1"  # Adjust pod type based on your needs
            )

        # Get the index instance
        index = Index(index_name)

        # Prepare the vectors for upsert
        vectors = [{"id": str(id_), "vector": embedding, "metadata": {"text_field": text}} 
                   for id_, embedding, text in zip(ids, embeddings, texts)]  # Assuming texts are available

        # Upsert the vectors into Pinecone
        index.upsert(vectors)

        return {"message": f"Upserted {len(embeddings)} vectors to Pinecone index '{index_name}'"}
    except Exception as e:
        print(f"Error upserting to Pinecone: {str(e)}")
        return {"error": str(e)}
