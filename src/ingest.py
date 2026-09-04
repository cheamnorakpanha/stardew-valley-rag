# Ingestion in Retrieval-Augmented Generation (RAG) is the offline preprocessing phase
# where raw source documents are collected, cleaned, broken down, and stored so an AI
# system can search through them later.

from pathlib import Path


DATA_DIR = Path("data")

EXCLUDED_FILES = {
    "README.md",
    "source_policy.md",
}


def load_documents():
    documents = []

    for file_path in DATA_DIR.glob("*.md"):
        if file_path.name in EXCLUDED_FILES:
            continue

        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print("=" * 50)
        print(f"Source: {document['source']}")
        print(document["text"][:300])
