# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer

from ingest import load_documents, create_chunks


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the embedding model.
    """

    model = SentenceTransformer(MODEL_NAME)

    return model


def create_embeddings(model, texts):
    """
    Convert texts into embeddings.
    """

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


if __name__ == "__main__":

    # Load and process documents
    documents = load_documents()

    chunks = create_chunks(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    # Extract text from chunks
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # Load embedding model
    model = load_embedding_model()

    # Create embeddings
    embeddings = create_embeddings(model, texts)

    print("\nEmbedding complete!")

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")

    # Display first chunk
    print("\nFirst chunk:")
    print("=" * 60)
    print(chunks[0]["text"])

    print("\nMetadata:")
    print(chunks[0]["metadata"])

    print("\nFirst embedding:")
    print(embeddings[0])
