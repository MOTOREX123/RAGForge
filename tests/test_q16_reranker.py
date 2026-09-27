from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker


db = VectorStore.load("vectorstore")

question = "What is underfitting in machine learning?"

hybrid = HybridRetriever(db)

candidates = hybrid.search(
    question,
    k=10,
    candidate_k=10
)

reranker = Reranker()

results = reranker.rerank(
    question,
    candidates,
    top_k=10
)

print()
print("RERANKED RESULTS")
print("=" * 60)

for i, result in enumerate(results, start=1):
    print(
        f"Rank {i} | "
        f"score={result['rerank_score']:.4f} | "
        f"source={result['source']} | "
        f"page={result['page']} | "
        f"chunk_id={result['chunk_id']}"
    )