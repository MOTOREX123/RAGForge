# from utils.vectorstore import VectorStore
# from utils.bm25_retriever import BM25Retriever
# from utils.hybrid_retriever import HybridRetriever
# from utils.reranker import Reranker
# from utils.embeddings import model

# from evaluation_dataset import evaluation_dataset


# VECTORSTORE_FOLDER = "vectorstore"


# def source_page_match(
#     result: dict,
#     expected_sources: list[str],
#     expected_pages: list[int]
# ) -> bool:

#     source_match = result["source"] in expected_sources
#     page_match = result["page"] in expected_pages

#     return source_match and page_match


# def evaluate_faiss(
#     vector_db,
#     question: str,
#     expected_sources: list[str],
#     expected_pages: list[int],
#     k: int = 5
# ):
#     query_embedding = model.encode(question)

#     results = vector_db.search(
#         query_embedding,
#         k=k
#     )

#     for result in results:
#         if source_page_match(
#             result,
#             expected_sources,
#             expected_pages
#         ):
#             return True

#     return False


# def evaluate_bm25(
#     bm25,
#     question: str,
#     expected_sources: list[str],
#     expected_pages: list[int],
#     k: int = 5
# ):
#     results = bm25.search(
#         question,
#         k=k
#     )

#     for result in results:
#         if source_page_match(
#             result,
#             expected_sources,
#             expected_pages
#         ):
#             return True

#     return False


# def evaluate_hybrid(
#     hybrid,
#     question: str,
#     expected_sources: list[str],
#     expected_pages: list[int],
#     k: int = 5
# ):
#     results = hybrid.search(
#         question,
#         k=k,
#         candidate_k=10
#     )

#     for result in results:
#         if source_page_match(
#             result,
#             expected_sources,
#             expected_pages
#         ):
#             return True

#     return False


# def evaluate_reranker(
#     hybrid,
#     reranker,
#     question: str,
#     expected_sources: list[str],
#     expected_pages: list[int],
#     candidate_k: int = 10,
#     top_k: int = 5
# ):
#     candidates = hybrid.search(
#         question,
#         k=candidate_k,
#         candidate_k=candidate_k
#     )

#     results = reranker.rerank(
#         question,
#         candidates,
#         top_k=top_k
#     )

#     for result in results:
#         if source_page_match(
#             result,
#             expected_sources,
#             expected_pages
#         ):
#             return True

#     return False


# def main():

#     print("=" * 70)
#     print("RAGFORGE RETRIEVAL EVALUATION")
#     print("=" * 70)

#     vector_db = VectorStore.load(
#         VECTORSTORE_FOLDER
#     )

#     print(
#         f"Loaded chunks: {len(vector_db.chunks)}"
#     )

#     bm25 = BM25Retriever(
#         vector_db.chunks
#     )

#     hybrid = HybridRetriever(
#         vector_db
#     )

#     reranker = Reranker()

#     results = []

#     for item in evaluation_dataset:

#         question = item["question"]
#         expected_sources = item["expected_sources"]
#         expected_pages = item["expected_pages"]

#         print()
#         print("-" * 70)
#         print(f"Question: {question}")

#         faiss_hit = evaluate_faiss(
#             vector_db,
#             question,
#             expected_sources,
#             expected_pages
#         )

#         bm25_hit = evaluate_bm25(
#             bm25,
#             question,
#             expected_sources,
#             expected_pages
#         )

#         hybrid_hit = evaluate_hybrid(
#             hybrid,
#             question,
#             expected_sources,
#             expected_pages
#         )

#         reranker_hit = evaluate_reranker(
#             hybrid,
#             reranker,
#             question,
#             expected_sources,
#             expected_pages
#         )

#         result = {
#             "question": question,
#             "faiss": faiss_hit,
#             "bm25": bm25_hit,
#             "hybrid": hybrid_hit,
#             "reranker": reranker_hit,
#         }

#         results.append(result)

#         print(f"FAISS:     {'HIT' if faiss_hit else 'MISS'}")
#         print(f"BM25:      {'HIT' if bm25_hit else 'MISS'}")
#         print(f"Hybrid:    {'HIT' if hybrid_hit else 'MISS'}")
#         print(f"Reranker:  {'HIT' if reranker_hit else 'MISS'}")

#     print()
#     print("=" * 70)
#     print("SUMMARY")
#     print("=" * 70)

#     total = len(results)

#     faiss_hits = sum(
#         result["faiss"]
#         for result in results
#     )

#     bm25_hits = sum(
#         result["bm25"]
#         for result in results
#     )

#     hybrid_hits = sum(
#         result["hybrid"]
#         for result in results
#     )

#     reranker_hits = sum(
#         result["reranker"]
#         for result in results
#     )

#     print(
#         f"FAISS:     {faiss_hits}/{total}"
#     )

#     print(
#         f"BM25:      {bm25_hits}/{total}"
#     )

#     print(
#         f"Hybrid:    {hybrid_hits}/{total}"
#     )

#     print(
#         f"Reranker:  {reranker_hits}/{total}"
#     )


# if __name__ == "__main__":
#     main()

from math import log2

from utils.vectorstore import VectorStore
from utils.bm25_retriever import BM25Retriever
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker
from utils.embeddings import model

from evaluation_dataset import evaluation_dataset


VECTORSTORE_FOLDER = "vectorstore"


# ============================================================
# Relevance
# ============================================================

def is_relevant(
    result: dict,
    expected_sources: list[str],
    expected_pages: list[int]
) -> bool:
    """
    A result is considered relevant when both:
    - its source matches an expected source
    - its page matches an expected page
    """

    source_match = result["source"] in expected_sources
    page_match = result["page"] in expected_pages

    return source_match and page_match


# ============================================================
# Retrieval functions
# ============================================================

def get_faiss_results(
    vector_db,
    question: str,
    k: int = 10
):
    query_embedding = model.encode(question)

    return vector_db.search(
        query_embedding,
        k=k
    )


def get_bm25_results(
    bm25,
    question: str,
    k: int = 10
):
    return bm25.search(
        question,
        k=k
    )


def get_hybrid_results(
    hybrid,
    question: str,
    k: int = 10
):
    return hybrid.search(
        question,
        k=k,
        candidate_k=10
    )


def get_reranker_results(
    hybrid,
    reranker,
    question: str,
    candidate_k: int = 10,
    top_k: int = 10
):
    candidates = hybrid.search(
        question,
        k=candidate_k,
        candidate_k=candidate_k
    )

    return reranker.rerank(
        question,
        candidates,
        top_k=top_k
    )


# ============================================================
# Ranking metrics
# ============================================================

def recall_at_k(
    results: list[dict],
    expected_sources: list[str],
    expected_pages: list[int],
    k: int
) -> bool:
    """
    Returns True if at least one relevant result
    appears within the first k results.
    """

    top_results = results[:k]

    return any(
        is_relevant(
            result,
            expected_sources,
            expected_pages
        )
        for result in top_results
    )


def reciprocal_rank(
    results: list[dict],
    expected_sources: list[str],
    expected_pages: list[int]
) -> float:
    """
    Reciprocal rank of the first relevant result.

    Rank 1 -> 1.0
    Rank 2 -> 0.5
    Rank 3 -> 0.333
    etc.
    """

    for rank, result in enumerate(results, start=1):

        if is_relevant(
            result,
            expected_sources,
            expected_pages
        ):
            return 1.0 / rank

    return 0.0


def precision_at_k(
    results: list[dict],
    expected_sources: list[str],
    expected_pages: list[int],
    k: int
) -> float:
    """
    Fraction of the top-k results that are relevant.
    """

    top_results = results[:k]

    if not top_results:
        return 0.0

    relevant_count = sum(
        is_relevant(
            result,
            expected_sources,
            expected_pages
        )
        for result in top_results
    )

    return relevant_count / len(top_results)


def ndcg_at_k(
    results: list[dict],
    expected_sources: list[str],
    expected_pages: list[int],
    k: int
) -> float:
    """
    Binary-relevance NDCG@K.

    Relevant result = 1
    Irrelevant result = 0
    """

    top_results = results[:k]

    if not top_results:
        return 0.0

    gains = [
        1 if is_relevant(
            result,
            expected_sources,
            expected_pages
        ) else 0
        for result in top_results
    ]

    dcg = sum(
        gain / log2(rank + 1)
        for rank, gain in enumerate(gains, start=1)
    )

    # Ideal ranking puts all relevant results first.
    relevant_count = sum(gains)

    ideal_gains = [
        1
        for _ in range(
            min(relevant_count, k)
        )
    ]

    idcg = sum(
        gain / log2(rank + 1)
        for rank, gain in enumerate(
            ideal_gains,
            start=1
        )
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg


# ============================================================
# Evaluation
# ============================================================

def evaluate_system(
    results: list[dict],
    expected_sources: list[str],
    expected_pages: list[int]
):
    return {
        "recall@1": recall_at_k(
            results,
            expected_sources,
            expected_pages,
            1
        ),

        "recall@3": recall_at_k(
            results,
            expected_sources,
            expected_pages,
            3
        ),

        "recall@5": recall_at_k(
            results,
            expected_sources,
            expected_pages,
            5
        ),

        "recall@10": recall_at_k(
            results,
            expected_sources,
            expected_pages,
            10
        ),

        "mrr@10": reciprocal_rank(
            results,
            expected_sources,
            expected_pages
        ),

        "precision@5": precision_at_k(
            results,
            expected_sources,
            expected_pages,
            5
        ),

        "ndcg@5": ndcg_at_k(
            results,
            expected_sources,
            expected_pages,
            5
        ),
    }


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("RAGFORGE RETRIEVAL EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load vector store
    # --------------------------------------------------------

    vector_db = VectorStore.load(
        VECTORSTORE_FOLDER
    )

    print(
        f"Loaded chunks: {len(vector_db.chunks)}"
    )

    # --------------------------------------------------------
    # Initialize retrievers
    # --------------------------------------------------------

    bm25 = BM25Retriever(
        vector_db.chunks
    )

    hybrid = HybridRetriever(
        vector_db
    )

    reranker = Reranker()

    # --------------------------------------------------------
    # Store evaluation results
    # --------------------------------------------------------

    all_results = {
        "FAISS": [],
        "BM25": [],
        "Hybrid": [],
        "Reranker": [],
    }

    # --------------------------------------------------------
    # Evaluate every question
    # --------------------------------------------------------

    for item in evaluation_dataset:

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
            f"Question: {question}"
        )

        # ----------------------------------------------------
        # FAISS
        # ----------------------------------------------------

        faiss_results = get_faiss_results(
            vector_db,
            question,
            k=10
        )

        faiss_metrics = evaluate_system(
            faiss_results,
            expected_sources,
            expected_pages
        )

        # ----------------------------------------------------
        # BM25
        # ----------------------------------------------------

        bm25_results = get_bm25_results(
            bm25,
            question,
            k=10
        )

        bm25_metrics = evaluate_system(
            bm25_results,
            expected_sources,
            expected_pages
        )

        # ----------------------------------------------------
        # Hybrid
        # ----------------------------------------------------

        hybrid_results = get_hybrid_results(
            hybrid,
            question,
            k=10
        )

        hybrid_metrics = evaluate_system(
            hybrid_results,
            expected_sources,
            expected_pages
        )

        # ----------------------------------------------------
        # Reranker
        # ----------------------------------------------------

        reranker_results = get_reranker_results(
            hybrid,
            reranker,
            question,
            candidate_k=10,
            top_k=10
        )

        reranker_metrics = evaluate_system(
            reranker_results,
            expected_sources,
            expected_pages
        )

        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------

        all_results["FAISS"].append(
            faiss_metrics
        )

        all_results["BM25"].append(
            bm25_metrics
        )

        all_results["Hybrid"].append(
            hybrid_metrics
        )

        all_results["Reranker"].append(
            reranker_metrics
        )

        # ----------------------------------------------------
        # Display basic hit results
        # ----------------------------------------------------

        print(
            f"FAISS:     "
            f"{'HIT' if faiss_metrics['recall@5'] else 'MISS'}"
        )

        print(
            f"BM25:      "
            f"{'HIT' if bm25_metrics['recall@5'] else 'MISS'}"
        )

        print(
            f"Hybrid:    "
            f"{'HIT' if hybrid_metrics['recall@5'] else 'MISS'}"
        )

        print(
            f"Reranker:  "
            f"{'HIT' if reranker_metrics['recall@5'] else 'MISS'}"
        )


    # ========================================================
    # Summary
    # ========================================================

    total = len(evaluation_dataset)

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    # --------------------------------------------------------
    # Recall summary
    # --------------------------------------------------------

    print()
    print("RECALL")

    print(
        f"{'System':<12}"
        f"{'R@1':>10}"
        f"{'R@3':>10}"
        f"{'R@5':>10}"
        f"{'R@10':>10}"
    )

    print("-" * 52)

    for system, metrics_list in all_results.items():

        r1 = sum(
            m["recall@1"]
            for m in metrics_list
        )

        r3 = sum(
            m["recall@3"]
            for m in metrics_list
        )

        r5 = sum(
            m["recall@5"]
            for m in metrics_list
        )

        r10 = sum(
            m["recall@10"]
            for m in metrics_list
        )

        print(
            f"{system:<12}"
            f"{r1:>5}/{total:<4}"
            f"{r3:>5}/{total:<4}"
            f"{r5:>5}/{total:<4}"
            f"{r10:>5}/{total:<4}"
        )


    # --------------------------------------------------------
    # MRR
    # --------------------------------------------------------

    print()
    print("MRR@10")
    print("-" * 52)

    for system, metrics_list in all_results.items():

        mrr = sum(
            m["mrr@10"]
            for m in metrics_list
        ) / total

        print(
            f"{system:<12}"
            f"{mrr:.4f}"
        )


    # --------------------------------------------------------
    # Precision
    # --------------------------------------------------------

    print()
    print("PRECISION@5")
    print("-" * 52)

    for system, metrics_list in all_results.items():

        precision = sum(
            m["precision@5"]
            for m in metrics_list
        ) / total

        print(
            f"{system:<12}"
            f"{precision:.4f}"
        )


    # --------------------------------------------------------
    # NDCG
    # --------------------------------------------------------

    print()
    print("NDCG@5")
    print("-" * 52)

    for system, metrics_list in all_results.items():

        ndcg = sum(
            m["ndcg@5"]
            for m in metrics_list
        ) / total

        print(
            f"{system:<12}"
            f"{ndcg:.4f}"
        )


if __name__ == "__main__":
    main()