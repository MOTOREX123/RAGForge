from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever


db = VectorStore.load("vectorstore")

hybrid = HybridRetriever(db)

results = hybrid.search(
    "What is a random forest?",
    k=10,
    candidate_k=10
)

print()
print("RANDOM FOREST HYBRID RETRIEVAL")
print("=" * 60)

for i, result in enumerate(results, start=1):
    print(
        f"{i}. {result['source']} "
        f"| p.{result['page']} "
        f"| chunk {result['chunk_id']} "
        f"| RRF {result['rrf_score']:.6f}"
    )