# Ingestion in Retrieval-Augmented Generation (RAG) is the offline preprocessing phase
# where raw source documents are collected, cleaned, broken down, and stored so an AI
# system can search through them later.

from pathlib import Path
import re


DATA_DIR = Path("data")

EXCLUDED_FILES = {
    "README.md",
    "source_policy.md",
}


def clean_text(text):
    # Remove trailing spaces from each line
    text = "\n".join(line.strip() for line in text.splitlines())

    # Replace 3 or more consecutive newlines with 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove unnecessary whitespace at the beginning/end
    text = text.strip()

    return text


def extract_metadata(file_path):
    category = file_path.stem

    return {
        "source": file_path.name,
        "category": category,
    }


def load_documents():
    documents = []

    for file_path in DATA_DIR.glob("*.md"):

        if file_path.name in EXCLUDED_FILES:
            continue

        raw_text = file_path.read_text(encoding="utf-8")

        cleaned_text = clean_text(raw_text)

        metadata = extract_metadata(file_path)

        documents.append({
            "text": cleaned_text,
            "metadata": metadata
        })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print("=" * 50)
        print(f"Metadata: {document['metadata']}")
        print(document["text"][:300])
