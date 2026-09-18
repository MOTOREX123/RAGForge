from utils.vectorstore import VectorStore
from utils.bm25_retriever import BM25Retriever


def main():
    print("=" * 60)
    print("BM25 RETRIEVER TEST")
    print("=" * 60)

    vector_db = VectorStore.load("vectorstore")

    print(f"Loaded chunks: {len(vector_db.chunks)}")

    bm25 = BM25Retriever(vector_db.chunks)

    question = "What is a convolutional neural network?"

    results = bm25.search(
        question,
        k=5
    )

    print()
    print(f"Query: {question}")
    print()

    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Text: {result['text'][:250]}")
        print("-" * 60)


if __name__ == "__main__":
    main()