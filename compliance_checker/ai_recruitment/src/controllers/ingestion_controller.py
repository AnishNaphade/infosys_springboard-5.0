from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks.

    Args:
        chunks (list): A list of text chunks.

    Returns:
        list: A list of embeddings, or an error message if the process fails.
    """

    try:
        embeddings = model.encode(chunks, show_progress_bar=True)
        return embeddings
    except Exception as e:
        logging.error(f"Embedding generation failed: {str(e)}")
        return {"error": f"Embedding generation failed: {str(e)}"}