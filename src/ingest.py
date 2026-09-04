from pathlib import Path
import re


# ============================================================
# Configuration
# ============================================================

DATA_DIR = Path("data")

EXCLUDED_FILES = {
    "README.md",
    "source_policy.md",
}


# ============================================================
# Step 3 — Clean Text
# ============================================================

def clean_text(text):
    """
    Clean unnecessary whitespace from extracted text.
    """

    # Remove spaces at the beginning/end of each line
    text = "\n".join(line.strip() for line in text.splitlines())

    # Replace 3+ consecutive newlines with 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove whitespace at beginning/end of document
    text = text.strip()

    return text


# ============================================================
# Step 4 — Extract Metadata
# ============================================================

def extract_metadata(file_path):
    """
    Create metadata for a document.
    """

    return {
        "source": file_path.name,
        "category": file_path.stem,
    }


# ============================================================
# Step 5 — Split Document into Chunks
# ============================================================

def split_into_chunks(text):
    """
    Split Markdown document into sections using ## headings.
    """

    sections = re.split(r"\n(?=## )", text)

    chunks = []

    for section in sections:

        section = section.strip()

        # Skip empty sections
        if not section:
            continue

        # Skip the main document title (# ...)
        if section.startswith("# ") and not section.startswith("## "):
            continue

        lines = section.splitlines()

        # First line should be the section title
        title = lines[0].replace("## ", "").strip()

        chunks.append({
            "text": section,
            "section": title,
        })

    return chunks


# ============================================================
# Step 2 — Ingest Documents
# ============================================================

def load_documents():
    """
    Read all Markdown documents from the data directory.
    """

    documents = []

    for file_path in DATA_DIR.glob("*.md"):

        # Ignore project documentation
        if file_path.name in EXCLUDED_FILES:
            continue

        # Read document
        raw_text = file_path.read_text(encoding="utf-8")

        # Clean document
        cleaned_text = clean_text(raw_text)

        # Extract metadata
        metadata = extract_metadata(file_path)

        documents.append({
            "text": cleaned_text,
            "metadata": metadata,
        })

    return documents


# ============================================================
# Create Chunks
# ============================================================

def create_chunks(documents):
    """
    Split every document into chunks
    and attach metadata to each chunk.
    """

    chunks = []

    for document in documents:

        sections = split_into_chunks(document["text"])

        for section in sections:

            # Copy document metadata
            metadata = document["metadata"].copy()

            # Add section metadata
            metadata["section"] = section["section"]

            chunks.append({
                "text": section["text"],
                "metadata": metadata,
            })

    return chunks


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    # Step 2: Load documents
    documents = load_documents()

    # Step 5: Create chunks
    chunks = create_chunks(documents)

    print("=" * 60)
    print("STARDew VALLEY RAG - INGESTION")
    print("=" * 60)

    print(f"Documents loaded : {len(documents)}")
    print(f"Chunks created   : {len(chunks)}")

    print("\nSample chunks:")
    print("=" * 60)

    for i, chunk in enumerate(chunks[:10]):

        print(f"\nChunk {i}")
        print("-" * 60)

        print("Metadata:")
        print(chunk["metadata"])

        print("\nText:")
        print(chunk["text"])
