from evaluation_dataset import evaluation_dataset
from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever
from utils.query_transformer import transform_query


VECTORSTORE_PATH = "vectorstore"


def is_relevant(result, item):
    return (
        result["source"] in item["expected_sources"]
        and result["page"] in item["expected_pages"]
    )


def first_relevant_rank(results, item, k=10):
    for rank, result in enumerate(results[:k], start=1):
        if is_relevant(result, item):
            return rank

    return None


def merge_results(query_results):
    """
    Merge results from the original query and rewrites.

    A chunk retrieved multiple times is kept only once.
    """

    merged = {}

    for results in query_results:
        for rank, result in enumerate(results, start=1):

            key = (
                result["source"],
                result["page"],
                result["chunk_id"],
            )

            score = result.get("rrf_score", 0.0)

            if key not in merged:
                merged[key] = {
                    **result,
                    "_best_score": score,
                }
            else:
                merged[key]["_best_score"] = max(
                    merged[key]["_best_score"],
                    score,
                )

    merged_results = list(merged.values())

    merged_results.sort(
        key=lambda x: x["_best_score"],
        reverse=True,
    )

    return merged_results


def main():

    print("=" * 70)
    print("QUERY TRANSFORMATION REGRESSION INSPECTION")
    print("=" * 70)

    vector_db = VectorStore.load(
        VECTORSTORE_PATH
    )

    print(f"Loaded chunks: {len(vector_db.chunks)}")

    hybrid_retriever = HybridRetriever(
        vector_db
    )

    regressions = []

    for index, item in enumerate(
        evaluation_dataset,
        start=1
    ):

        question = item["question"]

        # -----------------------------
        # Original query
        # -----------------------------

        original_results = hybrid_retriever.search(
            question,
            k=10,
            candidate_k=10,
        )

        original_rank = first_relevant_rank(
            original_results,
            item,
        )

        # -----------------------------
        # Transformed queries
        # -----------------------------

        queries = transform_query(question)

        query_results = []

        for query in queries:

            results = hybrid_retriever.search(
                query,
                k=10,
                candidate_k=10,
            )

            query_results.append(results)

        transformed_results = merge_results(
            query_results
        )

        transformed_rank = first_relevant_rank(
            transformed_results,
            item,
        )

        # -----------------------------
        # Detect regression
        # -----------------------------

        original_value = (
            original_rank
            if original_rank is not None
            else 999
        )

        transformed_value = (
            transformed_rank
            if transformed_rank is not None
            else 999
        )

        if transformed_value > original_value:

            regressions.append({
                "question": question,
                "queries": queries,
                "original_rank": original_rank,
                "transformed_rank": transformed_rank,
                "original_results": original_results,
                "transformed_results": transformed_results,
            })

    # -----------------------------
    # Print regressions
    # -----------------------------

    print()
    print("=" * 70)
    print(
        f"REGRESSIONS FOUND: {len(regressions)}"
    )
    print("=" * 70)

    for index, item in enumerate(
        regressions,
        start=1
    ):

        print()
        print("-" * 70)

        print(
            f"[{index}/{len(regressions)}] "
            f"{item['question']}"
        )

        print()

        print("Queries used:")

        for query in item["queries"]:
            print(f"  - {query}")

        print()

        print(
            f"Original first relevant rank: "
            f"{item['original_rank']}"
        )

        print(
            f"Transformed first relevant rank: "
            f"{item['transformed_rank']}"
        )

        print()

        print("Original top results:")

        for rank, result in enumerate(
            item["original_results"][:5],
            start=1
        ):

            relevant = is_relevant(
                result,
                evaluation_dataset[
                    next(
                        i
                        for i, x in enumerate(evaluation_dataset)
                        if x["question"] == item["question"]
                    )
                ],
            )

            marker = "✓" if relevant else " "

            print(
                f"  {rank}. [{marker}] "
                f"{result['source']} "
                f"p.{result['page']} "
                f"score={result.get('rrf_score', 0):.4f}"
            )

        print()

        print("Transformed top results:")

        for rank, result in enumerate(
            item["transformed_results"][:5],
            start=1
        ):

            relevant = (
                result["source"]
                in evaluation_dataset[
                    next(
                        i
                        for i, x in enumerate(evaluation_dataset)
                        if x["question"] == item["question"]
                    )
                ]["expected_sources"]
                and
                result["page"]
                in evaluation_dataset[
                    next(
                        i
                        for i, x in enumerate(evaluation_dataset)
                        if x["question"] == item["question"]
                    )
                ]["expected_pages"]
            )

            marker = "✓" if relevant else " "

            print(
                f"  {rank}. [{marker}] "
                f"{result['source']} "
                f"p.{result['page']} "
                f"score={result.get('_best_score', 0):.4f}"
            )


if __name__ == "__main__":
    main()