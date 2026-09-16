"""FastAPI application for the RAG knowledge assistant demo."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .chunking import chunk_markdown
from .retrieval import HybridIndex

app = FastAPI(title="Enterprise RAG Knowledge Assistant", version="1.0.0")
index = HybridIndex()


class DocumentRequest(BaseModel):
    source: str = Field(min_length=1)
    content: str = Field(min_length=1)


class QueryRequest(BaseModel):
    question: str = Field(min_length=2)
    top_k: int = Field(default=3, ge=1, le=10)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/documents")
def add_document(request: DocumentRequest) -> dict:
    chunks = chunk_markdown(request.content, request.source)
    index.add(chunks)
    return {"source": request.source, "chunks_added": len(chunks)}


@app.post("/search")
def search(request: QueryRequest) -> dict:
    return {"results": index.search(request.question, request.top_k)}


@app.post("/ask")
def ask(request: QueryRequest) -> dict:
    results = index.search(request.question, request.top_k)
    if not results:
        raise HTTPException(status_code=404, detail="No relevant knowledge found")
    context = " ".join(result["text"] for result in results)
    citations = [f'{result["source"]}#{result["section"]}' for result in results]
    return {
        "answer": f"Grounded context: {context}",
        "citations": citations,
        "note": "Connect an approved LLM provider to synthesize a production answer.",
    }
