from utils.bm25_retriever import BM25Retriever


class HybridRetriever:
    """
    Combines semantic retrieval (FAISS) and
    keyword retrieval (BM25) using Reciprocal
    Rank Fusion (RRF).
    """

    def __init__(self, vector_db):
        self.vector_db = vector_db

        # Build BM25 using the same chunks
        # already stored in FAISS.
        self.bm25 = BM25Retriever(
            vector_db.chunks
        )

    def search(
        self,
        query: str,
        k: int = 5,
        candidate_k: int = 10,
        rrf_k: int = 60
    ) -> list[dict]:
        """
        Retrieve candidates using both FAISS and BM25,
        then combine their rankings using RRF.
        """

        # -------------------------------------------------
        # 1. FAISS semantic retrieval
        # -------------------------------------------------

        from utils.embeddings import model

        query_embedding = model.encode(query)

        faiss_results = self.vector_db.search(
            query_embedding,
            k=candidate_k
        )

        # -------------------------------------------------
        # 2. BM25 keyword retrieval
        # -------------------------------------------------

        bm25_results = self.bm25.search(
            query,
            k=candidate_k
        )

        # -------------------------------------------------
        # 3. RRF score calculation
        # -------------------------------------------------

        fused_results = {}

        # FAISS rankings
        for rank, result in enumerate(
            faiss_results,
            start=1
        ):
            chunk_id = result["chunk_id"]

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    "chunk": result.copy(),
                    "rrf_score": 0.0
                }

            fused_results[chunk_id]["rrf_score"] += (
                1 / (rrf_k + rank)
            )

        # BM25 rankings
        for rank, result in enumerate(
            bm25_results,
            start=1
        ):
            chunk_id = result["chunk_id"]

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    "chunk": result.copy(),
                    "rrf_score": 0.0
                }

            fused_results[chunk_id]["rrf_score"] += (
                1 / (rrf_k + rank)
            )

        # -------------------------------------------------
        # 4. Sort by combined RRF score
        # -------------------------------------------------

        ranked_results = sorted(
            fused_results.values(),
            key=lambda item: item["rrf_score"],
            reverse=True
        )

        # -------------------------------------------------
        # 5. Return top k results
        # -------------------------------------------------

        results = []

        for item in ranked_results[:k]:

            chunk = item["chunk"].copy()

            chunk["rrf_score"] = item["rrf_score"]

            results.append(chunk)

        return results