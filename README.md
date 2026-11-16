# LangChain Course: RAG Gist (`rag-gist` branch)

Code from the Udemy LangChain course. This branch is a minimal Retrieval-Augmented Generation (RAG) pipeline:

1. Take a text file (a Medium blog post), split it into chunks, embed them, and store them in a Pinecone vector index.
2. Ask a question, retrieve the most relevant chunks from Pinecone, and have an LLM answer using only that context.

The question-answering step is written twice, once by hand and once with LCEL (LangChain Expression Language), so the two styles can be compared.

## Stack

| Piece | Choice |
|---|---|
| Language / tooling | Python 3.12, [uv](https://docs.astral.sh/uv/) |
| Framework | LangChain (`langchain`, `langchain-core`, `langchain-text-splitters`) |
| LLM | Google Gemini via `langchain-google-genai` (`gemini-3.5-flash-lite`) |
| Embeddings | Google `gemini-embedding-2` (3072 dimensions) |
| Vector store | Pinecone serverless (`langchain-pinecone`), AWS `us-east-1`, cosine metric |
| Document loading | `langchain-unstructured` (`UnstructuredLoader`) |
| Tracing (optional) | LangSmith |

## Project layout

```
.
├── create_index.py     # Creates (or recreates) the Pinecone index
├── ingestion.py        # Loads, splits, embeds and uploads mediumblog.txt
├── main.py             # Question answering: non-LCEL and LCEL implementations
├── mediumblog.txt      # Source document that gets ingested
├── src/langchain_course/   # Package stub from `uv init`, not used by the scripts
├── static/             # LangChain / LangGraph logo images
├── pyproject.toml      # Dependencies
└── uv.lock
```

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Create a `.env` file in the project root (it is gitignored). Variables used by the code in this branch:

   | Variable | Purpose |
   |---|---|
   | `GOOGLE_API_KEY` | Gemini chat and embedding models |
   | `PINECONE_API_KEY` | Pinecone access |
   | `INDEX_NAME` | Name of the Pinecone index to create and use |

   The `.env` may also hold `LANGSMITH_*` (tracing) and `TAVILY_API_KEY` (web search). Those are not used here; they belong to other branches of the course.

## How to run

Run these in order the first time:

```bash
uv run python create_index.py   # 1. create the index
uv run python ingestion.py      # 2. embed and upload the blog post
uv run python main.py           # 3. ask a question
```

### `create_index.py`

Creates a dense Pinecone index named `INDEX_NAME` with `dimension=3072` and `metric="cosine"`. **If an index with that name already exists, it is deleted and recreated**, so all stored vectors are lost. The dimension must match the embedding model's output size (3072 for `gemini-embedding-2`); change one and you must change the other.

### `ingestion.py`

1. `UnstructuredLoader` reads `mediumblog.txt` (`chunking_strategy="basic"`, `max_characters=1000000`, so effectively one large element per section).
2. `CharacterTextSplitter` splits it into chunks of 1000 characters with no overlap.
3. `PineconeVectorStore.from_documents` embeds each chunk with Gemini and uploads it to the index.

Running it twice adds the same chunks again (duplicates). Recreate the index with `create_index.py` first if you want a clean state.

### `main.py`

Builds a retriever (`k=3`, the top three chunks) on the Pinecone index and a prompt that tells the model to answer based only on the retrieved context. It then runs the same query (`"What is Pinecone in Machine Learning?"`) through two implementations:

- **`retrieval_chain_without_lcel(query)`**: manual steps. Retrieve documents, join them into a context string, format the prompt, call the LLM, return `response.content`. Simple, but no built-in streaming, async or batching.
- **`create_retrieval_chain_with_lcel()`**: a declarative chain:
  ```python
  RunnablePassthrough.assign(
      context = itemgetter("question") | retriever | format_docs
  ) | prompt_template | llm | StrOutputParser()
  ```
  Invoked with `{"question": ...}`. `RunnablePassthrough.assign` keeps the input and adds a `context` key; `itemgetter("question")` pulls the question out of the input dict to feed the retriever; `StrOutputParser` turns the `AIMessage` into a plain string. This version gets streaming, async and batching for free.

Change the `query` variable at the bottom of `main.py` to ask something else.

## Notes and gotchas

- The model names (`gemini-3.5-flash-lite`, `gemini-embedding-2`) are set directly in the code. If a call fails with a "model not found" error, check the current names in the Google docs.
- `pyproject.toml` declares a `langchain-course` script entry point and `src/langchain_course/`, but that is leftover scaffolding. Everything runs through the top-level scripts.
- `HumanMessage` is imported in `main.py` but unused.

## Other branches

The repo has one branch per course section: `main`, `project/hello-world`, `agents-under-the-hood`, `search-agent` and this one, `rag-gist`.
