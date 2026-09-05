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

def create_question_embedding(model, question):
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

def build_augmented_prompt(question, results):
    """
    Combine the user's question with the
    retrieved chunks to create an augmented prompt.
    """

    retrieved_documents = results["documents"][0]

    context = "\n\n".join(
        retrieved_documents
    )

    prompt = f"""
    You are a Stardew Valley assistant.

    Answer the user's question using only the
    provided context.

    Give a helpful and moderately detailed answer.
    Explain the important points clearly and use
    bullet points when appropriate.

    Do not add information that is not supported
    by the provided context.

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

def generate_rag_response(question, results):
    """
    Build the augmented prompt and send it
    to the LLM.
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
# Main CLI
# ============================================================

def main():

    print("=" * 60)
    print("🌾 Stardew Valley Assistant")
    print("=" * 60)

    # Step 8: Receive question
    question = get_user_question()

    # Step 9: Create question embedding
    print("\n🔎 Searching knowledge base...")

    model = load_embedding_model()

    question_embedding = create_question_embedding(
        model,
        question
    )

    # Connect to ChromaDB
    collection = get_collection()

    # Step 10: Retrieve relevant chunks
    results = retrieve_chunks(
        collection,
        question_embedding,
        n_results=N_RESULTS
    )

    # Step 11 + Step 13:
    # Build augmented prompt and generate response
    print("🤖 Generating answer...")

    response = generate_rag_response(
        question,
        results
    )

    # Display final answer
    print("\nAssistant:")
    print("-" * 60)
    print(response)

    print("\n" + "=" * 60)


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":
    main()
