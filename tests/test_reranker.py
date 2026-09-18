from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker


def main():

    print("=" * 60)
    print("RERANKER TEST")
    print("=" * 60)

    # --------------------------------------------
    # Load existing vector store
    # --------------------------------------------

    vector_db = VectorStore.load(
        "vectorstore"
    )

    print(
        f"Loaded chunks: {len(vector_db.chunks)}"
    )

    # --------------------------------------------
    # Create hybrid retriever
    # --------------------------------------------

    hybrid = HybridRetriever(
        vector_db
    )

    question = "What is overfitting?"

    print()
    print(
        "Step 1: Retrieving candidates..."
    )

    candidates = hybrid.search(
        question,
        k=10,
        candidate_k=10
    )

    print(
        f"Candidates retrieved: "
        f"{len(candidates)}"
    )

    # --------------------------------------------
    # Create reranker
    # --------------------------------------------

    print()
    print(
        "Step 2: Loading reranker..."
    )

    reranker = Reranker()

    # --------------------------------------------
    # Rerank
    # --------------------------------------------

    print()
    print(
        "Step 3: Reranking candidates..."
    )

    results = reranker.rerank(
        question,
        candidates,
        top_k=5
    )

    # --------------------------------------------
    # Display results
    # --------------------------------------------

    print()
    print(
        f"Query: {question}"
    )

    print()

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"Result {i}"
        )

        print(
            f"Rerank Score: "
            f"{result['rerank_score']:.4f}"
        )

        print(
            f"RRF Score: "
            f"{result['rrf_score']:.6f}"
        )

        print(
            f"Source: "
            f"{result['source']}"
        )

        print(
            f"Page: "
            f"{result['page']}"
        )

        print(
            f"Chunk ID: "
            f"{result['chunk_id']}"
        )

        print(
            f"Text: "
            f"{result['text'][:300]}"
        )

        print(
            "-" * 60
        )


if __name__ == "__main__":
    main()