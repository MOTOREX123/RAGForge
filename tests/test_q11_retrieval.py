from utils.vectorstore import VectorStore
from utils.retriever import retrieve_chunks
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker


QUESTION = "What is backpropagation used for in neural network training?"


print("=" * 70)
print("Q11 RETRIEVAL DIAGNOSTIC")
print("=" * 70)

print("\nLoading vector store...")
vector_db = VectorStore.load("vectorstore")

print(f"Loaded chunks: {len(vector_db.chunks)}")


# ---------------------------------------------------------
# 1. FAISS retrieval
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("FAISS TOP 10")
print("=" * 70)

faiss_results = retrieve_chunks(
    vector_db,
    QUESTION,
    k=10,
    threshold=0.0
)

for rank, result in enumerate(faiss_results, start=1):
    print(
        f"\n{rank}. "
        f"chunk={result['chunk_id']} | "
        f"page={result['page']} | "
        f"score={result['score']:.4f}"
    )
    print(result["text"][:500].replace("\n", " "))


# ---------------------------------------------------------
# 2. Hybrid retrieval
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("HYBRID TOP 10")
print("=" * 70)

hybrid = HybridRetriever(vector_db)

hybrid_results = hybrid.search(
    QUESTION,
    k=10,
    candidate_k=10,
    faiss_results=faiss_results
)

for rank, result in enumerate(hybrid_results, start=1):
    print(
        f"\n{rank}. "
        f"chunk={result['chunk_id']} | "
        f"page={result['page']} | "
        f"rrf={result['rrf_score']:.6f}"
    )
    print(result["text"][:500].replace("\n", " "))


# ---------------------------------------------------------
# 3. Reranker
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("RERANKER TOP 10")
print("=" * 70)

reranker = Reranker()

reranked_results = reranker.rerank(
    QUESTION,
    hybrid_results,
    top_k=10
)

for rank, result in enumerate(reranked_results, start=1):
    print(
        f"\n{rank}. "
        f"chunk={result['chunk_id']} | "
        f"page={result['page']} | "
        f"rerank={result['rerank_score']:.4f}"
    )
    print(result["text"][:500].replace("\n", " "))


print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)