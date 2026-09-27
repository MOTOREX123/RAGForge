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
    3. Prefer one chunk per source/page.
    4. Avoid duplicate chunks.
    5. Fill remaining slots if necessary.
    """

    selected = []
    seen_chunks = set()
    seen_pages = set()
    remaining = []

    for result in results:
        score = result.get("rerank_score", float("-inf"))

        if score < min_score:
            continue

        chunk_key = (
            result["source"],
            result["chunk_id"]
        )

        page_key = (
            result["source"],
            result["page"]
        )

        if chunk_key in seen_chunks:
            continue

        seen_chunks.add(chunk_key)

        if page_key not in seen_pages:
            selected.append(result)
            seen_pages.add(page_key)

            if len(selected) >= max_chunks:
                break
        else:
            remaining.append(result)

    # If we still need more chunks, use remaining candidates.
    if len(selected) < max_chunks:
        for result in remaining:
            if result not in selected:
                selected.append(result)

            if len(selected) >= max_chunks:
                break

    return selected