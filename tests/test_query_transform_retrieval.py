from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever
from utils.query_transformer import transform_query
from utils.embeddings import model

from evaluation_dataset import evaluation_dataset


VECTORSTORE_FOLDER = "vectorstore"


def is_relevant(
    result: dict,
    expected_sources: list[str],
    expected_pages: list[int]
) -> bool:

    return (
        result["source"] in expected_sources
        and result["page"] in expected_pages
    )


def retrieve_with_query(
    vector_db,
    hybrid,
    query: str,
    k: int = 5
):
    """
    Run the existing hybrid retriever using one query.
    """

    query_embedding = model.encode(query)

    faiss_results = vector_db.search(
        query_embedding,
        k=10
    )

    return hybrid.search(
        query,
        k=k,
        candidate_k=10,
        faiss_results=faiss_results
    )


def merge_results(result_lists: list[list[dict]]) -> list[dict]:
    """
    Merge results from multiple transformed queries.

    A chunk is kept only once.
    """

    merged = {}

    for results in result_lists:

        for result in results:

            key = (
                result["source"],
                result["page"],
                result["chunk_id"]
            )

            if key not in merged:

                merged[key] = result

    return list(merged.values())


def main():

    print("=" * 70)
    print("RAGFORGE QUERY TRANSFORMATION RETRIEVAL TEST")
    print("=" * 70)

    vector_db = VectorStore.load(
        VECTORSTORE_FOLDER
    )

    print(
        f"Loaded chunks: {len(vector_db.chunks)}"
    )

    hybrid = HybridRetriever(
        vector_db
    )

    original_hits = 0
    transformed_hits = 0

    total = len(evaluation_dataset)

    for index, item in enumerate(
        evaluation_dataset,
        start=1
    ):

        question = item["question"]

        expected_sources = item[
            "expected_sources"
        ]

        expected_pages = item[
            "expected_pages"
        ]

        print()
        print("-" * 70)
        print(
            f"[{index}/{total}] {question}"
        )

        # ====================================================
        # ORIGINAL QUERY
        # ====================================================

        original_results = retrieve_with_query(
            vector_db,
            hybrid,
            question,
            k=5
        )

        original_hit = any(
            is_relevant(
                result,
                expected_sources,
                expected_pages
            )
            for result in original_results
        )

        # ====================================================
        # TRANSFORMED QUERIES
        # ====================================================

        queries = transform_query(
            question
        )

        print()
        print("Queries:")

        for query in queries:
            print(f"  - {query}")

        transformed_result_lists = []

        for query in queries:

            results = retrieve_with_query(
                vector_db,
                hybrid,
                query,
                k=5
            )

            transformed_result_lists.append(
                results
            )

        transformed_results = merge_results(
            transformed_result_lists
        )

        transformed_hit = any(
            is_relevant(
                result,
                expected_sources,
                expected_pages
            )
            for result in transformed_results
        )

        # ====================================================
        # RESULT
        # ====================================================

        if original_hit:
            original_hits += 1

        if transformed_hit:
            transformed_hits += 1

        print()
        print(
            f"Original query:    "
            f"{'HIT' if original_hit else 'MISS'}"
        )

        print(
            f"Transformed query: "
            f"{'HIT' if transformed_hit else 'MISS'}"
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print()
    print(
        f"Original Hybrid:     "
        f"{original_hits}/{total}"
    )

    print(
        f"Query Transformed:   "
        f"{transformed_hits}/{total}"
    )

    print()

    improvement = (
        transformed_hits - original_hits
    )

    if improvement > 0:

        print(
            f"Improvement: +{improvement} questions"
        )

    elif improvement < 0:

        print(
            f"Change: {improvement} questions"
        )

    else:

        print(
            "Change: no difference"
        )


if __name__ == "__main__":
    main()