from utils.vectorstore import VectorStore
from utils.retriever import retrieve_chunks
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker
from utils.chunk_expander import expand_neighbors


QUESTION = "What is backpropagation used for in neural network training?"

print("=" * 70)
print("Q11 EXPANSION DIAGNOSTIC")
print("=" * 70)

vector_db = VectorStore.load("vectorstore")

# ---------------------------------------------------------
# Retrieve
# ---------------------------------------------------------
faiss_results = retrieve_chunks(
    vector_db,
    QUESTION,
    k=10,
    threshold=0.0
)

hybrid = HybridRetriever(vector_db)

candidates = hybrid.search(
    QUESTION,
    k=10,
    candidate_k=10,
    faiss_results=faiss_results
)

# ---------------------------------------------------------
# Rerank
# ---------------------------------------------------------
reranker = Reranker()

results = reranker.rerank(
    QUESTION,
    candidates,
    top_k=5
)

print("\nRERANKED RESULTS")
print("=" * 70)

for rank, result in enumerate(results, start=1):
    print(
        f"{rank}. "
        f"chunk={result['chunk_id']} | "
        f"page={result['page']} | "
        f"rerank={result['rerank_score']:.4f}"
    )


# ---------------------------------------------------------
# CURRENT: expand top 1
# ---------------------------------------------------------
current = expand_neighbors(
    vector_db,
    [results[0]],
    before=0,
    after=3
)

print("\nCURRENT: TOP 1 EXPANSION")
print("=" * 70)

for chunk in current:
    print(
        f"chunk={chunk['chunk_id']} | "
        f"page={chunk['page']} | "
        f"expanded_from={chunk['expanded_from']}"
    )


# ---------------------------------------------------------
# PROPOSED: expand top 3
# ---------------------------------------------------------
proposed = expand_neighbors(
    vector_db,
    results[:3],
    before=0,
    after=3
)

print("\nPROPOSED: TOP 3 EXPANSION")
print("=" * 70)

for chunk in proposed:
    print(
        f"chunk={chunk['chunk_id']} | "
        f"page={chunk['page']} | "
        f"expanded_from={chunk['expanded_from']}"
    )


# ---------------------------------------------------------
# Show relevant text from proposed context
# ---------------------------------------------------------
print("\nPROPOSED CONTEXT TEXT")
print("=" * 70)

for chunk in proposed:
    print(
        f"\n--- chunk {chunk['chunk_id']} | "
        f"page {chunk['page']} ---"
    )
    print(chunk["text"][:1000])


print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
