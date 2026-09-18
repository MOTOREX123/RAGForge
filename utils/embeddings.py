from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks: list[dict]):
    """
    Create embeddings from chunk text.
    """

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(texts)

    return embeddings