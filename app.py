"""
app.py

FastAPI server for MultiDocumentRAG.

This file is the API / presentation layer ONLY.
All retrieval, routing, embedding, FAISS, and LLM logic lives in
utils/ and is imported here unchanged.

Do NOT put RAG/business logic in this file beyond simple glue code
(building the citation-aware context string, shaping JSON responses).

main.py remains the CLI entrypoint and is untouched by this file.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal, Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from utils.vectorstore import VectorStore
from utils.router import route_query
from utils.ollama_llm import (
    generate_ollama_answer,
    generate_general_answer,
    OLLAMA_URL,
    MODEL_NAME
)
from utils.web_search import web_search

from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker


# ==========================================================
# APP STATE
# ==========================================================
# The FAISS-backed VectorStore is expensive to load (reads index.faiss +
# chunks.json from disk). It must be loaded exactly ONCE at process
# startup, not per-request. We store it on `app.state`.

PROJECT_ROOT = Path(__file__).resolve().parent
VECTORSTORE_FOLDER = PROJECT_ROOT / "vectorstore"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("LOADING RAG SYSTEM")
    print("=" * 60)

    # -----------------------------------------
    # 1. Load FAISS vector store
    # -----------------------------------------

    print("Loading vector store...")

    app.state.vector_db = VectorStore.load(
        str(VECTORSTORE_FOLDER)
    )

    print(
        f"Loaded chunks: "
        f"{len(app.state.vector_db.chunks)}"
    )

    print(
        f"Embedding dimension: "
        f"{app.state.vector_db.dimension}"
    )

    # -----------------------------------------
    # 2. Build Hybrid Retriever
    # -----------------------------------------

    print("Building hybrid retriever...")

    app.state.hybrid_retriever = HybridRetriever(
        app.state.vector_db
    )

    print("Hybrid retriever ready.")

    # -----------------------------------------
    # 3. Load Cross-Encoder Reranker
    # -----------------------------------------

    print("Loading reranker...")

    app.state.reranker = Reranker()

    print("Reranker ready.")

    print("=" * 60)
    print("RAG SYSTEM READY")
    print("=" * 60)

    yield

    # No explicit teardown needed.

    # No explicit teardown needed for FAISS/in-memory chunks.


app = FastAPI(
    title="MultiDocumentRAG API",
    description="API layer over the existing MultiDocumentRAG pipeline "
                 "(FAISS + Ollama/Gemma + Gemini web search).",
    version="0.1.0",
    lifespan=lifespan,
)

# ==========================================================
# CORS
# ==========================================================
# Allow the local Vite dev server to call this API during development.
# Adjust/extend origins as needed when deploying.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# REQUEST / RESPONSE MODELS
# ==========================================================

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's chat message.")
    conversation_id: Optional[str] = Field(
        default=None,
        description="Optional conversation identifier (not yet used for memory).",
    )


class Citation(BaseModel):
    id: int
    type: Literal["document", "web"]
    source: str
    page: Optional[int] = None
    score: Optional[float] = None
    url: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    route: Literal["local", "web","general"]
    provider: Literal["ollama", "gemini"]
    model: str
    citations: list[Citation]


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    vectorstore_loaded: bool
    chunk_count: Optional[int] = None
    ollama_reachable: bool


# ==========================================================
# HELPERS
# ==========================================================

def build_context(results: list[dict]) -> str:
    """
    Build the same citation-aware context string that main.py builds
    before calling generate_ollama_answer(). Kept identical in shape
    so Ollama's citation behavior (referencing [1], [2], ...) matches
    what main.py already produces.
    """
    context_parts = []

    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"""
    [{i}]
    Source: {result['source']}
    Page: {result['page']}

    {result['text']}
    """
        )

    return "\n\n".join(context_parts)


def local_results_to_citations(results: list[dict]) -> list[Citation]:
    citations = []
    for i, result in enumerate(results, start=1):
        citations.append(
            Citation(
                id=i,
                type="document",
                source=result["source"],
                page=result.get("page"),
                score=result.get("rerank_score"),
                url=None,
            )
        )
    return citations


def web_sources_to_citations(sources: list[dict]) -> list[Citation]:
    citations = []
    for i, source in enumerate(sources, start=1):
        citations.append(
            Citation(
                id=i,
                type="web",
                source=source.get("title", "Unknown source"),
                page=None,
                score=None,
                url=source.get("url"),
            )
        )
    return citations


def check_ollama_reachable() -> bool:
    try:
        # Lightweight reachability check against Ollama's base API.
        base_url = OLLAMA_URL.replace("/api/chat", "")
        resp = requests.get(f"{base_url}/api/tags", timeout=3)
        return resp.status_code == 200
    except requests.RequestException:
        return False


# ==========================================================
# ROUTES
# ==========================================================

@app.get("/api/health", response_model=HealthResponse)
def health():
    vector_db = getattr(app.state, "vector_db", None)
    vectorstore_loaded = vector_db is not None
    chunk_count = len(vector_db.chunks) if vectorstore_loaded else None
    ollama_ok = check_ollama_reachable()

    status = "ok" if (vectorstore_loaded and ollama_ok) else "degraded"

    return HealthResponse(
        status=status,
        vectorstore_loaded=vectorstore_loaded,
        chunk_count=chunk_count,
        ollama_reachable=ollama_ok,
    )


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip() if request.message else ""

    if not message:
        raise HTTPException(status_code=400, detail="message must not be empty.")

    vector_db = getattr(app.state, "vector_db", None)
    if vector_db is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store is not loaded. Server may still be starting up.",
        )

    # ------------------------------------------------------
    # ROUTING (unchanged logic from utils/router.py)
    # ------------------------------------------------------
    try:
        route = route_query(
            vector_db,
            message,
            k=8,
            threshold=0.50,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Routing failed: {exc}",
        ) from exc

    # ------------------------------------------------------
    # LOCAL ROUTE
    # ------------------------------------------------------

    if route["source"] == "local":

        hybrid_retriever = app.state.hybrid_retriever
        reranker = app.state.reranker

        # -----------------------------------------
        # Step 1: Hybrid retrieval
        # -----------------------------------------

        candidates = hybrid_retriever.search(
            message,
            k=10,
            candidate_k=10,
            faiss_results=route["results"]
        )

        # -----------------------------------------
        # Step 2: Rerank candidates
        # -----------------------------------------

        results = reranker.rerank(
            message,
            candidates,
            top_k=5
        )

        # -----------------------------------------
        # Step 3: Build context
        # -----------------------------------------

        context = build_context(results)

        # -----------------------------------------
        # Step 4: Generate answer
        # -----------------------------------------

        try:
            answer = generate_ollama_answer(
                message,
                context
            )

        except requests.RequestException as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Ollama is unavailable: {exc}",
            ) from exc

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error generating answer: {exc}",
            ) from exc

        # -----------------------------------------
        # Step 5: Return response
        # -----------------------------------------

        return ChatResponse(
            answer=answer,
            route="local",
            provider="ollama",
            model=MODEL_NAME,
            citations=local_results_to_citations(results),
        )

    # ------------------------------------------------------
    # GENERAL ROUTE
    # ------------------------------------------------------
    if route["source"] == "general":
        try:
            answer = generate_general_answer(message)
        except requests.RequestException as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Ollama is unavailable: {exc}",
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error generating answer: {exc}",
            ) from exc

        return ChatResponse(
            answer=answer,
            route="general",
            provider="ollama",
            model=MODEL_NAME,
            citations=[],
        )

    # ------------------------------------------------------
    # WEB ROUTE
    # ------------------------------------------------------
    try:
        result = web_search(message)
    except Exception as exc:
        # Covers Gemini quota errors, network failures, API errors, etc.
        raise HTTPException(
            status_code=502,
            detail=f"Web search (Gemini) failed: {exc}",
        ) from exc

        return ChatResponse(
            answer=result["answer"],
            route="web",
            provider="gemini",
            model="gemini-3.6-flash",
            citations=web_sources_to_citations(result.get("sources", [])),
        )


# ==========================================================
# PLACEHOLDER ENDPOINTS (honest 501s — no fake data)
# ==========================================================

@app.get("/api/documents")
def list_documents():
    raise HTTPException(
        status_code=501,
        detail="Document listing is not implemented yet.",
    )


@app.post("/api/upload")
def upload_document():
    raise HTTPException(
        status_code=501,
        detail="Document upload is not implemented yet.",
    )


@app.delete("/api/documents/{document_id}")
def delete_document(document_id: str):
    raise HTTPException(
        status_code=501,
        detail=f"Document deletion is not implemented yet (id={document_id}).",
    )
