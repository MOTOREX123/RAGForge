from collections import defaultdict

from evaluation_dataset import evaluation_dataset
from utils.vectorstore import VectorStore
from utils.hybrid_retriever import HybridRetriever
from utils.query_transformer import transform_query


VECTORSTORE_PATH = "vectorstore"


def is_relevant(result, item):
    """
    A retrieved chunk is relevant when both its source
    and page match the evaluation ground truth.
    """

    source_match = result["source"] in item["expected_sources"]
    page_match = result["page"] in item["expected_pages"]

    return source_match and page_match


def recall_at_k(results, item, k):
    """
    Recall@K for our single-target evaluation.

    Returns 1 if at least one relevant result appears
    in the top K, otherwise 0.
    """

    return int(
        any(
            is_relevant(result, item)
            for result in results[:k]
        )
    )


def reciprocal_rank(results, item, k=10):
    """
    Reciprocal Rank up to K.

    If the first relevant result is at rank r:
        RR = 1 / r

    If no relevant result exists in top K:
        RR = 0
    """

    for rank, result in enumerate(results[:k], start=1):
        if is_relevant(result, item):
            return 1 / rank

    return 0.0


def precision_at_k(results, item, k=5):
    """
    Precision@K = relevant results / K.
    """

    top_results = results[:k]

    if not top_results:
        return 0.0

    relevant_count = sum(
        is_relevant(result, item)
        for result in top_results
    )

    return relevant_count / len(top_results)


def dcg_at_k(results, item, k=5):
    """
    Discounted Cumulative Gain using binary relevance.
    """

    score = 0.0

    for rank, result in enumerate(results[:k], start=1):

        if is_relevant(result, item):
            score += 1 / __import__("math").log2(rank + 1)

    return score


def ndcg_at_k(results, item, k=5):
    """
    NDCG@K using binary relevance.
    """

    actual_dcg = dcg_at_k(results, item, k)

    # Number of relevant documents available in the result set.
    relevant_available = sum(
        is_relevant(result, item)
        for result in results
    )

    ideal_relevant = min(relevant_available, k)

    ideal_dcg = sum(
        1 / __import__("math").log2(rank + 1)
        for rank in range(1, ideal_relevant + 1)
    )

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def merge_transformed_results(query_results):
    """
    Merge retrieval results from the original question
    and its transformed queries.

    The same chunk can be retrieved by multiple queries.
    We keep one copy of each chunk.

    For ranking, the best RRF score obtained across
    query variants is used.
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


def calculate_metrics(results_by_question):
    """
    Calculate all retrieval metrics.
    """

    metrics = {
        "R@1": [],
        "R@3": [],
        "R@5": [],
        "R@10": [],
        "MRR@10": [],
        "P@5": [],
        "NDCG@5": [],
    }

    for results, item in results_by_question:

        metrics["R@1"].append(
            recall_at_k(results, item, 1)
        )

        metrics["R@3"].append(
            recall_at_k(results, item, 3)
        )

        metrics["R@5"].append(
            recall_at_k(results, item, 5)
        )

        metrics["R@10"].append(
            recall_at_k(results, item, 10)
        )

        metrics["MRR@10"].append(
            reciprocal_rank(results, item, 10)
        )

        metrics["P@5"].append(
            precision_at_k(results, item, 5)
        )

        metrics["NDCG@5"].append(
            ndcg_at_k(results, item, 5)
        )

    question_count = len(results_by_question)

    return {
        metric: sum(values) / question_count
        for metric, values in metrics.items()
    }


def run_original_hybrid(vector_db, hybrid_retriever):
    """
    Run the original question through Hybrid Retrieval.
    """

    results_by_question = []

    for item in evaluation_dataset:

        question = item["question"]

        results = hybrid_retriever.search(
            question,
            k=10,
            candidate_k=10,
        )

        results_by_question.append(
            (results, item)
        )

    return results_by_question


def run_query_transformation(vector_db, hybrid_retriever):
    """
    Run the original question plus two transformed
    queries through Hybrid Retrieval.

    Results from all query variants are merged.
    """

    results_by_question = []

    for index, item in enumerate(evaluation_dataset, start=1):

        question = item["question"]

        print(
            f"[{index}/{len(evaluation_dataset)}] "
            f"{question}"
        )

        queries = transform_query(question)

        query_results = []

        for query in queries:

            results = hybrid_retriever.search(
                query,
                k=10,
                candidate_k=10,
            )

            query_results.append(results)

        merged_results = merge_transformed_results(
            query_results
        )

        results_by_question.append(
            (merged_results, item)
        )

    return results_by_question


def print_metrics(title, metrics):
    """
    Display evaluation metrics.
    """

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    for metric, value in metrics.items():

        if metric.startswith("R@"):
            print(
                f"{metric:<10} "
                f"{value:.4f} "
                f"({round(value * len(evaluation_dataset))}/"
                f"{len(evaluation_dataset)})"
            )

        else:
            print(
                f"{metric:<10} "
                f"{value:.4f}"
            )


def main():

    print("=" * 70)
    print("RAGFORGE QUERY TRANSFORMATION EVALUATION")
    print("=" * 70)

    print()
    print("Loading vector store...")

    vector_db = VectorStore.load(
        VECTORSTORE_PATH
    )

    print(
        f"Loaded chunks: {len(vector_db.chunks)}"
    )

    print()
    print("Building hybrid retriever...")

    hybrid_retriever = HybridRetriever(
        vector_db
    )

    print("Hybrid retriever ready.")

    # --------------------------------------------------
    # ORIGINAL HYBRID
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("1. ORIGINAL HYBRID")
    print("=" * 70)

    original_results = run_original_hybrid(
        vector_db,
        hybrid_retriever,
    )

    original_metrics = calculate_metrics(
        original_results
    )

    print_metrics(
        "ORIGINAL HYBRID RESULTS",
        original_metrics,
    )

    # --------------------------------------------------
    # QUERY TRANSFORMATION + HYBRID
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("2. QUERY TRANSFORMATION + HYBRID")
    print("=" * 70)

    transformed_results = run_query_transformation(
        vector_db,
        hybrid_retriever,
    )

    transformed_metrics = calculate_metrics(
        transformed_results
    )

    print_metrics(
        "QUERY TRANSFORMATION RESULTS",
        transformed_metrics,
    )

    # --------------------------------------------------
    # COMPARISON
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("COMPARISON")
    print("=" * 70)

    print()

    print(
        f"{'Metric':<12}"
        f"{'Original':>12}"
        f"{'Transformed':>15}"
        f"{'Change':>12}"
    )

    print("-" * 51)

    for metric in original_metrics:

        original = original_metrics[metric]
        transformed = transformed_metrics[metric]

        change = transformed - original

        print(
            f"{metric:<12}"
            f"{original:>12.4f}"
            f"{transformed:>15.4f}"
            f"{change:>+12.4f}"
        )


if __name__ == "__main__":
    main()