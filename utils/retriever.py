from utils.embeddings import model
from utils.vectorstore import VectorStore


def retrieve_chunks(
    vector_db: VectorStore,
    question: str,
    k: int = 8,
    threshold: float = 0.50
):
    """
    Retrieve relevant chunks from the vector store.

    First retrieves more candidates from FAISS,
    then removes low-similarity results and returns
    the best relevant chunks.
    """

    # Create embedding for the question
    query_embedding = model.encode(question)

    # Retrieve more candidates from FAISS
    results = vector_db.search(
        query_embedding,
        k=k
    )

    # Filter out weak matches
    filtered_results = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    # Keep the strongest results
    filtered_results = filtered_results[:k]

    return filtered_results