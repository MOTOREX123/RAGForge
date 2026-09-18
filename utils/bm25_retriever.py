from rank_bm25 import BM25Okapi
import re


class BM25Retriever:
    """
    Keyword-based retriever using the BM25 algorithm.

    It searches the existing document chunks using
    lexical/keyword matching rather than embeddings.
    """

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        tokenized_documents = [
            self.tokenize(document)
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """
        Convert text into clean lowercase tokens.
        """

        return re.findall(r"\b\w+\b", text.lower())

    def search(
        self,
        query: str,
        k: int = 5
    ) -> list[dict]:
        """
        Search the BM25 index and return the top k chunks.
        """

        query_tokens = self.tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for index in ranked_indexes[:k]:
            chunk = self.chunks[index].copy()

            chunk["score"] = float(scores[index])

            results.append(chunk)

        return results