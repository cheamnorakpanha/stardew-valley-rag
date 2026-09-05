# Stardew Valley RAG

A simple local Retrieval-Augmented Generation (RAG) application for
answering Stardew Valley questions using a local knowledge base.

The project is built from scratch with Python, Sentence Transformers,
ChromaDB, and Ollama. It does not use LangChain.

## Project Goal

The goal of this project is to understand and implement the complete RAG
pipeline step by step:

1.  Prepare the project
2.  Ingest and parse documents
3.  Clean extracted text
4.  Extract and attach metadata
5.  Split documents into chunks
6.  Create embeddings
7.  Build records and store them in a vector database
8.  Receive a user question
9.  Create a question embedding
10. Retrieve relevant chunks
11. Build an augmented prompt
12. Connect to an LLM
13. Generate a response
14. Complete the CLI application

## Architecture

```text
Markdown Documents
        |
        v
   Ingest Documents
        |
        v
    Clean Text
        |
        v
 Extract Metadata
        |
        v
    Split Text
        |
        v
 Create Embeddings
        |
        v
     ChromaDB
        |
        |
        +-----------------------------+
                                      |
User Question                         |
        |                             |
        v                             |
Question Embedding                    |
        |                             |
        v                             |
Similarity Search --------------------+
        |
        v
Retrieved Chunks
        |
        v
Augmented Prompt
        |
        v
Ollama
        |
        v
qwen3.5:4b
        |
        v
Final Answer
```

## Technologies

- Python
- Sentence Transformers
- `all-MiniLM-L6-v2`
- ChromaDB
- Ollama
- Qwen3.5 4B
- Markdown
- `tiktoken`

## Project Structure

```text
stardew-valley-rag/
|
├── data/
│   ├── source_policy.md
│   ├── stardew_guide_book.md
│   └── ultimate_stardew_valley_completion_guide.md
|
├── chroma_db/
│   └── ...
|
├── src/
│   ├── ingest.py
│   ├── embedding.py
│   ├── vector_db.py
│   ├── query.py
│   └── llm.py
|
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Data

The RAG knowledge base currently uses two Markdown documents:

- `stardew_guide_book.md`
- `ultimate_stardew_valley_completion_guide.md`

`source_policy.md` is excluded from ingestion because it contains
source-management information rather than Stardew Valley knowledge
intended for retrieval.

## Chunking

The ingestion pipeline:

- Cleans extracted Markdown text
- Detects `##` and `###` sections
- Keeps small sections together
- Splits large sections into token-based chunks
- Uses a target chunk size of 450 tokens
- Uses 70 tokens of overlap
- Adds source and section context to the embedded text

Example embedded context:

```text
Source: stardew_guide_book.md
Section: Welcome to the Valley!

## Welcome to the Valley!

...
```

The metadata stored with each chunk includes:

```python
{
    "source": "stardew_guide_book.md",
    "category": "stardew_guide_book",
    "section": "Welcome to the Valley!",
    "chunk_part": 1  # Optional: included when a section is split into multiple parts
}
```

## Embeddings

The project uses:

```text
all-MiniLM-L6-v2
```

The embedding size is:

```text
384 dimensions
```

The same embedding model is used for:

- Document chunks
- User questions

This allows the question embedding to be compared with document
embeddings in ChromaDB.

## Vector Database

ChromaDB is used as the local vector database.

Database path:

```text
chroma_db/
```

Collection name:

```text
stardew_valley
```

The current database contains the generated document chunks.

## Retrieval

When the user asks a question:

1.  The question is converted into an embedding.
2.  ChromaDB performs a similarity search.
3.  The most relevant chunks are retrieved.
4.  The retrieved text is combined into context.
5.  The context is passed to the LLM together with the question.

The current retrieval configuration uses:

```python
N_RESULTS = 10
```

The project intentionally uses generic semantic retrieval rather than
manually hard-coded Stardew-specific ranking rules.

## Augmented Prompt

The retrieved chunks are inserted into a prompt similar to:

```text
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
[retrieved chunks]
--------------------

Question:
[user question]

Answer:
```

This is the key step that turns normal generation into
Retrieval-Augmented Generation.

## LLM

The project uses Ollama as the local LLM runtime.

Current model:

```text
qwen3.5:4b
```

The Python package is:

```text
ollama
```

The LLM generation configuration currently uses:

```python
MAX_OUTPUT_TOKENS = 1500
```

and:

```python
think=False
```

The Ollama generation option is:

```python
"num_predict": MAX_OUTPUT_TOKENS
```

## CLI

The final application can be started with:

```powershell
python src/query.py
```

Example:

```text
============================================================
🌾 Stardew Valley Assistant
============================================================
You: What should I focus on during my first week in Stardew Valley?

🔎 Searching knowledge base...
🤖 Generating answer...

Assistant:
------------------------------------------------------------
Based on the provided context, here is what you should
focus on during your first week...
============================================================
```

The application hides the retrieved chunks and augmented prompt from the
normal user interface while still using them internally.

## Example Questions

The RAG has been tested with questions such as:

```text
What should I focus on during my first week in Stardew Valley?
```

```text
What should I do during winter?
```

```text
What does the guide recommend about upgrading tools?
```

The system successfully retrieved relevant context and generated answers
for these questions.

## Important RAG Principle

The LLM should use the retrieved context as its knowledge source.

The prompt explicitly tells the model not to add information that is
unsupported by the retrieved context.

This helps reduce hallucination, although the final system should still
be evaluated because a local LLM may sometimes use information from its
pretrained knowledge.

## Running the Project

### 1. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Make sure Ollama is running and model is available

Pull the model (if not already downloaded):

```powershell
ollama pull qwen3.5:4b
```

Check installed models:

```powershell
ollama list
```

### 4. Build or rebuild the ChromaDB database

If the documents or chunking logic change, rebuild the database.

```powershell
Remove-Item -Recurse -Force chroma_db
python src/vector_db.py
```

### 5. Run the RAG application

```powershell
python src/query.py
```

## Development Workflow

When changing the source Markdown documents or chunking configuration:

```text
Markdown files
      |
      v
ingest.py
      |
      v
Chunks
      |
      v
embedding.py
      |
      v
Embeddings
      |
      v
vector_db.py
      |
      v
ChromaDB
```

After rebuilding the database:

```text
query.py
    |
    +--> Question embedding
    |
    +--> ChromaDB retrieval
    |
    +--> Augmented prompt
    |
    +--> Ollama
    |
    +--> Final answer
```

## Current Status

All 14 planned steps have been implemented:

Step Description Status

---

1 Prepare Project Complete
2 Ingest & Parse Documents Complete
3 Clean Extracted Text Complete
4 Extract & Attach Metadata Complete
5 Split Documents into Chunks Complete
6 Create Embeddings Complete
7 Store in Vector DB Complete
8 Receive User Question Complete
9 Create Question Embedding Complete
10 Retrieve Relevant Chunks Complete
11 Build Augmented Prompt Complete
12 Connect to LLM Complete
13 Generate Response Complete
14 Complete CLI Application Complete

## Future Improvements

Possible improvements after the basic RAG is understood and evaluated:

- Evaluate retrieval quality with a larger set of questions
- Add source citations to final answers
- Improve document coverage
- Improve chunking if retrieval tests reveal weaknesses
- Add conversation history
- Add a CLI loop for multiple questions in one session
- Add retrieval debugging mode
- Add automated evaluation of retrieval and answer quality

These improvements should be added only after evaluating the current
baseline.

## License

This project is for learning and experimentation.
