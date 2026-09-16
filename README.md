# Enterprise RAG Knowledge Assistant

A portfolio-ready reference implementation of an enterprise knowledge assistant built with FastAPI, hybrid retrieval, structure-aware document chunking, and grounded answer generation.

## Problem it solves

Teams often spend too much time searching across long policies, manuals, and knowledge-base documents. This project retrieves the most relevant approved passages through semantic and keyword signals, reranks them, and returns grounded answers with source references.

> This is a sanitized demonstration based on professional project experience. It contains no employer source code, confidential documents, customer data, or production credentials.

## Highlights

- FastAPI service with health, ingestion, search, and answer endpoints
- Structure-aware Markdown chunking that preserves section headings
- Hybrid keyword and semantic-style retrieval with configurable weighting
- Deterministic reranking and source citations
- Dependency-light local demo; adapters can be replaced with Azure OpenAI and Azure AI Search
- Unit tests for chunking, ranking, and API behavior

## Architecture

1. Documents are split into section-aware chunks.
2. Each chunk is enriched with metadata and stored in an in-memory index.
3. Queries are scored using keyword overlap and lightweight vector similarity.
4. The highest-scoring chunks are reranked and returned as grounded context.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API.

## Example

```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"source":"leave-policy.md","content":"# Leave Policy\nEmployees receive 20 paid leave days per year."}'

curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How many paid leave days are available?","top_k":3}'
```

## Production extension points

- Replace the local index with Azure AI Search.
- Replace deterministic embeddings with Azure OpenAI embeddings.
- Add identity-aware retrieval, prompt guardrails, evaluation datasets, and observability.
- Add Gmail, Calendar, Google Chat, and multi-agent BI integrations behind permission-scoped tools.

## Author

Nagendra — AI Engineer specializing in Generative AI, RAG, agents, and production-oriented Python services.
