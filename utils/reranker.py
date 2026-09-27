from sentence_transformers import CrossEncoder


class Reranker:
    """
    Reranks retrieved document chunks using
    a Cross-Encoder model.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        print(
            f"Loading reranker model: {model_name}"
        )

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 5
    ) -> list[dict]:
        """
        Rerank retrieved chunks according to
        their relevance to the query.
        """

        if not results:
            return []

        pairs = [
            (
                query,
                result["text"]
            )
            for result in results
        ]

        scores = self.model.predict(pairs, batch_size=2)

        reranked_results = []

        for result, score in zip(
            results,
            scores
        ):
            updated_result = result.copy()

            updated_result["rerank_score"] = float(
                score
            )

            reranked_results.append(
                updated_result
            )

        reranked_results.sort(
            key=lambda result: result["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k]