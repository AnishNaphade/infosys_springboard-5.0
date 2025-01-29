from src.models.controllers.upload_controller import app as upload_app
from src.models.controllers.ingestion_controller import extract_text_from_pdf
from src.models.controllers.chunk_controller import chunk_text
from src.models.controllers.embedding_controller import generate_embeddings
from src.models.controllers.vector_controller import create_faiss_index, save_faiss_index
from src.models.controllers.pinecone_controller import upsert_to_pinecone
import os

# PDF upload folder
UPLOAD_FOLDER = 'data/uploads'

# FAISS index folder
FAISS_FOLDER = 'data/vector_store'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FAISS_FOLDER, exist_ok=True)

# Pinecone setup
INDEX_NAME = "pdf-compliance-index"

def process_pdf_pipeline(filepath, use_pinecone=False):
    """
    Processes a PDF file through the pipeline, extracting text, chunking,
    generating embeddings, and storing them in Pinecone or a local FAISS index.

    Args:
        filepath (str): The path to the PDF file.
        use_pinecone (bool, optional): Whether to store embeddings in Pinecone. Defaults to False.
    """

    print("\n--- Starting PDF Processing Pipeline ---\n")

    # Step 1: Extract text from PDF
    print("[1/5] Extracting text...")
    text = extract_text_from_pdf(filepath)
    print("Text extraction complete.")

    # Step 2: Chunk the text
    print("[2/5] Chunking text...")
    chunks = chunk_text(text)
    print(f"Text chunked into {len(chunks)} chunks.")

    # Step 3: Generate embeddings
    print("[3/5] Generating embeddings...")
    embeddings = generate_embeddings(chunks)
    print("Embeddings generated.")

    # Step 4: Store embeddings
    if use_pinecone:
        print("[4/5] Upserting embeddings to Pinecone...")
        upsert_to_pinecone(INDEX_NAME, embeddings, ids=range(len(chunks)))
        print("Embeddings uploaded to Pinecone.")
    else:
        print("[4/5] Creating FAISS index...")
        index = create_faiss_index(embeddings)
        save_faiss_index(index, path=os.path.join(FAISS_FOLDER, "index.faiss"))  # Specify path
        print("FAISS index saved locally.")

    print("\n--- Pipeline Complete ---\n")


if __name__ == "__main__":
    # Run the Flask API for uploading files
    upload_app.run(debug=True)

    # For testing, process a file directly
    test_filepath = 'data/uploads/sample.pdf'  # Replace with your test PDF
    process_pdf_pipeline(test_filepath, use_pinecone=False)