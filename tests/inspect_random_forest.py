from utils.vectorstore import VectorStore


db = VectorStore.load("vectorstore")

target_chunks = {1015, 1017, 1019, 1020, 1025}

for chunk in db.chunks:
    if chunk["chunk_id"] in target_chunks:
        print("=" * 80)
        print(
            f"{chunk['source']} | "
            f"page {chunk['page']} | "
            f"chunk {chunk['chunk_id']}"
        )
        print("=" * 80)
        print(chunk["text"])
        print()