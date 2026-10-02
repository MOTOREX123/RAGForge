import json
from pathlib import Path
import sys
sys.path.insert(0, r'D:\project\New folder (2)\RAGForge')

from utils.vectorstore import VectorStore
from utils.router import route_query
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker
from utils.context_selector import select_context

def safe_print(text):
    """Print text handling encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))

# Load vector store
PROJECT_ROOT = Path(__file__).resolve().parent
VECTORSTORE_FOLDER = PROJECT_ROOT / "vectorstore"

print("=" * 60)
print("LOADING VECTOR STORE")
print("=" * 60)

vector_db = VectorStore.load(str(VECTORSTORE_FOLDER))
print(f"Loaded chunks: {len(vector_db.chunks)}")
print(f"Embedding dimension: {vector_db.dimension}")

question = "What is depth-first search and what is one limitation of depth-first search?"

print("\n" + "=" * 60)
print("STEP 1: ROUTE QUERY")
print("=" * 60)

route = route_query(vector_db, question, k=8, threshold=0.50)
print(f"Route: {route['source']}")
print(f"Reason: {route['reason']}")
print(f"Initial FAISS results: {len(route['results'])}")

print("\n" + "=" * 60)
print("STEP 2: HYBRID RETRIEVER")
print("=" * 60)

hybrid_retriever = HybridRetriever(vector_db)
candidates = hybrid_retriever.search(
    question,
    k=10,
    candidate_k=10,
    faiss_results=route["results"]
)
print(f"Candidates after RRF: {len(candidates)}")

print("\n" + "=" * 60)
print("STEP 3: RERANKER")
print("=" * 60)

reranker = Reranker()
results = reranker.rerank(question, candidates, top_k=5)
print(f"Results after reranking: {len(results)}")

print("\n" + "=" * 60)
print("STEP 4: SELECT CONTEXT")
print("=" * 60)

selected_results = select_context(results, max_chunks=3, min_score=0.0)
print(f"Selected results: {len(selected_results)}")

print("\n" + "=" * 60)
print("FINAL SELECTED CHUNKS (with full text)")
print("=" * 60)

for i, r in enumerate(selected_results, 1):
    print(f"\n--- CHUNK {i} ---")
    print(f"Source: {r['source']}")
    print(f"Page: {r['page']}")
    print(f"Chunk ID: {r['chunk_id']}")
    print(f"Rerank Score: {r['rerank_score']:.4f}")
    print(f"Full Text:")
    safe_print(r['text'])
    print()

print("\n" + "=" * 60)
print("CONTEXT STRING SENT TO OLLAMA")
print("=" * 60)

def build_context(results):
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

context = build_context(selected_results)
safe_print(context)