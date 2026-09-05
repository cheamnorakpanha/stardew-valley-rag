from pathlib import Path
import re

# pyrefly: ignore [missing-import]
import tiktoken


# ============================================================
# Configuration
# ============================================================

DATA_DIR = Path("data")

EXCLUDED_FILES = {
    "README.md",
    "source_policy.md",
}

# Target chunk size
CHUNK_SIZE = 450

# Approximately 15% overlap
CHUNK_OVERLAP = 70

# Tokenizer used to measure chunk size
TOKENIZER = tiktoken.get_encoding("cl100k_base")


# ============================================================
# Step 3: Clean Extracted Text
# ============================================================

def clean_text(text):
    """
    Clean unnecessary whitespace from extracted text.
    """

    # Remove trailing spaces from each line
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    # Replace 3+ consecutive newlines with 2
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # Remove whitespace at beginning/end
    text = text.strip()

    return text


# ============================================================
# Step 4: Extract Metadata
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
# Token Utilities
# ============================================================

def count_tokens(text):
    """
    Count the number of tokens in a text.
    """

    return len(
        TOKENIZER.encode(text)
    )


# ============================================================
# Step 5: Recursive Token-Based Splitting
# ============================================================

def recursive_split(
    text,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
):
    """
    Split large text into token-based chunks.

    Target:
        ~450 tokens per chunk

    Overlap:
        ~70 tokens between chunks
    """

    tokens = TOKENIZER.encode(text)

    # If the text already fits, don't split it
    if len(tokens) <= chunk_size:
        return [text]

    chunks = []

    start = 0

    while start < len(tokens):

        end = min(
            start + chunk_size,
            len(tokens)
        )

        chunk_tokens = tokens[start:end]

        chunk_text = TOKENIZER.decode(
            chunk_tokens
        ).strip()

        if chunk_text:
            chunks.append(chunk_text)

        # Stop if we reached the end
        if end >= len(tokens):
            break

        # Move backward to create overlap
        start = end - overlap

    return chunks


# ============================================================
# Markdown-Aware Chunking
# ============================================================

def split_into_chunks(text):
    """
    Split Markdown documents using a hybrid strategy.

    Strategy:

    1. Split the document using Markdown ## and ### headings.
    2. Keep small sections intact.
    3. Recursively split large sections.
    4. Preserve the section title as metadata.
    """

    # Split whenever a ## or ### heading begins.
    sections = re.split(
        r"\n(?=#{2,3} )",
        text
    )

    chunks = []

    for section in sections:

        section = section.strip()

        if not section:
            continue

        # ----------------------------------------------------
        # Skip the document-level title
        # ----------------------------------------------------

        if (
            section.startswith("# ")
            and not section.startswith("## ")
        ):
            continue

        # ----------------------------------------------------
        # Extract section title
        # ----------------------------------------------------

        lines = section.splitlines()

        title = lines[0].lstrip("#").strip()

        # ----------------------------------------------------
        # Skip generic sections
        # ----------------------------------------------------

        if title.lower() in {
            "overview",
            "sources",
            "common examples",
        }:
            continue

        # ----------------------------------------------------
        # Count tokens
        # ----------------------------------------------------

        token_count = count_tokens(section)

        # ----------------------------------------------------
        # Small section
        # ----------------------------------------------------

        if token_count <= CHUNK_SIZE:

            chunks.append({
                "text": section,
                "section": title,
            })

        # ----------------------------------------------------
        # Large section
        # ----------------------------------------------------

        else:

            sub_chunks = recursive_split(
                section,
                chunk_size=CHUNK_SIZE,
                overlap=CHUNK_OVERLAP
            )

            for i, sub_chunk in enumerate(
                sub_chunks,
                start=1
            ):

                chunks.append({
                    "text": sub_chunk,
                    "section": title,
                    "chunk_part": i,
                })

    return chunks


# ============================================================
# Step 2: Load Documents
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

        # Read Markdown file
        raw_text = file_path.read_text(
            encoding="utf-8"
        )

        # Clean document
        cleaned_text = clean_text(
            raw_text
        )

        # Extract metadata
        metadata = extract_metadata(
            file_path
        )

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

        sections = split_into_chunks(
            document["text"]
        )

        for section in sections:

            # Copy document metadata
            metadata = document[
                "metadata"
            ].copy()

            # Add section metadata
            metadata["section"] = (
                section["section"]
            )

            # Add chunk part if the section
            # was split into multiple chunks
            if "chunk_part" in section:

                metadata["chunk_part"] = (
                    section["chunk_part"]
                )

            chunks.append({
                "text": section["text"],
                "metadata": metadata,
            })

    return chunks


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Step 2: Load documents
    # --------------------------------------------------------

    documents = load_documents()

    # --------------------------------------------------------
    # Step 5: Create chunks
    # --------------------------------------------------------

    chunks = create_chunks(
        documents
    )

    # --------------------------------------------------------
    # Display summary
    # --------------------------------------------------------

    print("=" * 60)
    print("STARDEW VALLEY RAG - INGESTION")
    print("=" * 60)

    print(
        f"Documents loaded : {len(documents)}"
    )

    print(
        f"Chunks created   : {len(chunks)}"
    )

    print(
        f"Target chunk size: {CHUNK_SIZE} tokens"
    )

    print(
        f"Chunk overlap    : {CHUNK_OVERLAP} tokens"
    )

    # --------------------------------------------------------
    # Display sample chunks
    # --------------------------------------------------------

    print("\nSample chunks:")
    print("=" * 60)

    for i, chunk in enumerate(
        chunks[:20]
    ):

        token_count = count_tokens(
            chunk["text"]
        )

        print(
            f"\nChunk {i}"
        )

        print("-" * 60)

        print("Metadata:")

        print(
            chunk["metadata"]
        )

        print(
            f"\nToken count: {token_count}"
        )

        print("\nText:")

        print(
            chunk["text"]
        )
