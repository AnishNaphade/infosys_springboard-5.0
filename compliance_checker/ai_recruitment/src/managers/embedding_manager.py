import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class Embedder:
    """
    Manages text embedding generation using a pre-trained sentence transformer model.

    Attributes:
        tokenizer (transformers.AutoTokenizer): The tokenizer for pre-processing text.
        model (transformers.AutoModel): The pre-trained sentence transformer model.
    """

    def __init__(self):
        """
        Loads the pre-trained model and tokenizer.
        """

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModel.from_pretrained(MODEL_NAME)

    def get_embeddings(self, chunks: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a list of text chunks.

        Args:
            chunks (list[str]): A list of text chunks to be embedded.

        Returns:
            list[list[float]]: A list of embedding vectors, one for each chunk.
                Each embedding vector is a list of floats.
        """

        embeddings = []
        for chunk in chunks:
            inputs = self.tokenizer(
                chunk, return_tensors="pt", truncation=True, padding=True
            )

            # Use `torch.no_grad()` for efficiency if embeddings are not used in backpropagation
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings.append(outputs.last_hidden_state.mean(dim=1).tolist())

        return embeddings


# Example usage
if __name__ == "__main__":
    embedder = Embedder()
    text_chunks = ["This is a short text.", "This is a longer text that needs embedding."]
    embeddings = embedder.get_embeddings(text_chunks)
    print(embeddings)