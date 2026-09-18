from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever


def main():

    print("=" * 60)
    print("HYBRID RETRIEVER TEST")
    print("=" * 60)

    # Load existing FAISS database
    vector_db = VectorStore.load(
        "vectorstore"
    )

    print(
        f"Loaded chunks: {len(vector_db.chunks)}"
    )

    # Create hybrid retriever
    hybrid = HybridRetriever(
        vector_db
    )

    question = "What is overfitting?"

    results = hybrid.search(
        question,
        k=5,
        candidate_k=10
    )

    print()
    print(f"Query: {question}")
    print()

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"Result {i}")

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
            f"{result['text'][:250]}"
        )

        print("-" * 60)


if __name__ == "__main__":
    main()