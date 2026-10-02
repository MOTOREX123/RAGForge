def select_context(
    results: list[dict],
    max_chunks: int = 3,
    min_score: float = 0.0
) -> list[dict]:
    """
    Select useful and diverse reranked chunks.

    Rules:
    1. Keep results in reranker order.
    2. Remove very low-scoring results.
    3. Avoid duplicate chunks.
    4. Return up to max_chunks.
    """

    selected = []
    seen_chunks = set()

    for result in results:
        score = result.get("rerank_score", float("-inf"))

        if score < min_score:
            continue

        chunk_key = (
            result["source"],
            result["chunk_id"]
        )

        if chunk_key in seen_chunks:
            continue

        seen_chunks.add(chunk_key)
        selected.append(result)

        if len(selected) >= max_chunks:
            break

    return selected