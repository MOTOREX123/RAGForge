def expand_neighbors(
    vector_db,
    results: list[dict],
    before: int = 1,
    after: int = 2
) -> list[dict]:

    expanded = []
    seen = set()

    for result in results:

        source = result["source"]
        chunk_id = result["chunk_id"]

        # Find neighboring chunks from the same source.
        neighbors = [
            chunk
            for chunk in vector_db.chunks
            if (
                chunk["source"] == source
                and abs(chunk["chunk_id"] - chunk_id) <= max(before, after)
            )
        ]

        # Keep only the requested directional range.
        neighbors = [
            chunk
            for chunk in neighbors
            if (
                (
                    chunk["chunk_id"] <= chunk_id
                    and chunk_id - chunk["chunk_id"] <= before
                )
                or
                (
                    chunk["chunk_id"] > chunk_id
                    and chunk["chunk_id"] - chunk_id <= after
                )
            )
        ]

        # Sort in document order.
        neighbors.sort(key=lambda chunk: chunk["chunk_id"])

        for chunk in neighbors:

            key = (
                chunk["source"],
                chunk["chunk_id"]
            )

            if key in seen:
                continue

            seen.add(key)

            expanded.append({
                **chunk,
                "expanded_from": chunk_id
            })

    return expanded