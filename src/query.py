import chromadb

from embedding import load_embedding_model, create_embeddings


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "stardew_valley"


def get_user_question():
    """
    Receive a question from the user.
    """

    question = input("You: ")

    return question


def create_question_embedding(model, question):
    """
    Convert the user's question into an embedding.
    """

    embedding = create_embeddings(
        model,
        [question]
    )

    return embedding[0]


def get_collection():
    """
    Connect to the existing ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def retrieve_chunks(collection, question_embedding, n_results=3):
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=n_results
    )

    return results


if __name__ == "__main__":

    # Step 8
    question = get_user_question()

    print("\nQuestion received:")
    print(question)

    # Step 9
    print("\nLoading embedding model...")

    model = load_embedding_model()

    question_embedding = create_question_embedding(
        model,
        question
    )

    print("Question embedding created!")

    # Step 10
    collection = get_collection()

    print("\nSearching ChromaDB...")

    results = retrieve_chunks(
        collection,
        question_embedding,
        n_results=10
    )

    print("\nRetrieved chunks:")
    print("=" * 60)

    for i, document in enumerate(results["documents"][0]):

        print(f"\nResult {i + 1}")
        print("-" * 60)

        print(document)

        print("\nMetadata:")
        print(results["metadatas"][0][i])
