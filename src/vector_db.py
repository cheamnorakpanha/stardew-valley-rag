import chromadb

from ingest import load_documents, create_chunks
from embedding import load_embedding_model, create_embeddings


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "stardew_valley"


def create_chroma_collection():
    """
    Create or load the Stardew Valley ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def store_chunks(collection, chunks, embeddings):
    """
    Store chunks, metadata, and embeddings in ChromaDB.
    """

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist()
    )

    return ids


if __name__ == "__main__":

    # ----------------------------------------
    # 1. Load documents
    # ----------------------------------------

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    # ----------------------------------------
    # 2. Create chunks
    # ----------------------------------------

    chunks = create_chunks(documents)

    print(f"Chunks created: {len(chunks)}")

    # ----------------------------------------
    # 3. Load embedding model
    # ----------------------------------------

    print("Loading embedding model...")

    model = load_embedding_model()

    # ----------------------------------------
    # 4. Extract chunk text
    # ----------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # ----------------------------------------
    # 5. Create embeddings
    # ----------------------------------------

    print("Creating embeddings...")

    embeddings = create_embeddings(
        model,
        texts
    )

    print("Embeddings created.")

    # ----------------------------------------
    # 6. Create ChromaDB collection
    # ----------------------------------------

    collection = create_chroma_collection()

    print("ChromaDB collection ready.")

    # ----------------------------------------
    # 7. Store everything
    # ----------------------------------------

    store_chunks(
        collection,
        chunks,
        embeddings
    )

    print("Chunks stored in ChromaDB.")

    # ----------------------------------------
    # 8. Check database
    # ----------------------------------------

    print(f"Total records: {collection.count()}")
