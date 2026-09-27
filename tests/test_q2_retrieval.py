from utils.vectorstore import VectorStore
from utils.router import route_query
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker


QUESTION = "What makes an AI agent rational?"

vector_db = VectorStore.load("vectorstore")

route = route_query(
    vector_db,
    QUESTION,
    k=10,
    threshold=0.65
)

print("\n" + "=" * 70)
print("ROUTE")
print("=" * 70)
print(route["source"])
print(route["reason"])

hybrid = HybridRetriever(vector_db)

candidates = hybrid.search(
    QUESTION,
    k=10,
    candidate_k=10,
    faiss_results=route["results"]
)

print("\n" + "=" * 70)
print("HYBRID RESULTS")
print("=" * 70)

for i, result in enumerate(candidates, start=1):
    print(
        f"\n{i}. "
        f"chunk={result['chunk_id']} "
        f"page={result['page']} "
        f"rrf={result['rrf_score']:.4f}"
    )
    print(result["text"][:500])


reranker = Reranker()

results = reranker.rerank(
    QUESTION,
    candidates,
    top_k=5
)

print("\n" + "=" * 70)
print("RERANKED RESULTS")
print("=" * 70)

for i, result in enumerate(results, start=1):
    print(
        f"\n{i}. "
        f"chunk={result['chunk_id']} "
        f"page={result['page']} "
        f"score={result.get('rerank_score')}"
    )
    print(result["text"][:700])