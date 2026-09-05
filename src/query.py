import chromadb

from embedding import load_embedding_model, create_embeddings
from llm import generate_response


# ============================================================
# Configuration
# ============================================================

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "stardew_valley"

N_RESULTS = 10


# ============================================================
# Step 8: Receive User Question
# ============================================================

def get_user_question():
    """
    Get a question from the user.
    """

    question = input("You: ")

    return question


# ============================================================
# Step 9: Create Question Embedding
# ============================================================

def create_question_embedding(
    model,
    question
):
    """
    Convert the user's question into an embedding.
    """

    embedding = create_embeddings(
        model,
        [question]
    )

    return embedding[0]


# ============================================================
# Connect to ChromaDB
# ============================================================

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


# ============================================================
# Step 10: Retrieve Relevant Chunks
# ============================================================

def retrieve_chunks(
    collection,
    question_embedding,
    n_results=N_RESULTS
):
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    return results


# ============================================================
# Step 11: Build Augmented Prompt
# ============================================================

def build_augmented_prompt(
    question,
    results
):
    """
    Combine the user's question with the
    retrieved chunks to create an augmented prompt.
    """

    retrieved_documents = results[
        "documents"
    ][0]

    # Combine retrieved chunks
    context = "\n\n".join(
        retrieved_documents
    )

    prompt = f"""
You are a Stardew Valley assistant.

Answer the user's question using only the
provided context.

If the context does not contain enough information
to answer the question, say that the information
is not available in the provided context.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
""".strip()

    return prompt


# ============================================================
# Step 13: Generate Response
# ============================================================

def generate_rag_response(
    question,
    results
):
    """
    Build the augmented prompt and send it
    to the LLM to generate the final answer.
    """

    prompt = build_augmented_prompt(
        question,
        results
    )

    response = generate_response(
        prompt
    )

    return response


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    # Step 8: Receive question
    question = get_user_question()

    print("\nQuestion received:")
    print(question)

    # Step 9: Create question embedding
    print("\nLoading embedding model...")

    model = load_embedding_model()

    question_embedding = create_question_embedding(
        model,
        question
    )

    print("Question embedding created!")

    # Connect to ChromaDB
    collection = get_collection()

    print("\nChromaDB collection loaded.")

    # Step 10: Retrieve relevant chunks
    print("\nSearching ChromaDB...")

    results = retrieve_chunks(
        collection,
        question_embedding,
        n_results=N_RESULTS
    )

    print(
        f"Retrieved {len(results['documents'][0])} chunks."
    )

    # Display retrieved chunks
    print("\nRetrieved chunks:")
    print("=" * 60)

    for i, document in enumerate(
        results["documents"][0]
    ):

        distance = results["distances"][0][i]

        print(
            f"\nResult {i + 1}"
        )

        print("-" * 60)

        print(
            f"Distance: {distance:.4f}"
        )

        print(document)

        print("\nMetadata:")

        print(
            results["metadatas"][0][i]
        )

    # Step 11: Build augmented prompt
    prompt = build_augmented_prompt(
        question,
        results
    )

    print("\n\nAugmented Prompt:")
    print("=" * 60)

    print(prompt)

    # Step 13: Generate final response
    print("\n\nGenerating response...")

    response = generate_response(
        prompt
    )

    print("\nFinal Answer:")
    print("=" * 60)

    print(response)
