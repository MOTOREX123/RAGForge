from utils.vectorstore import VectorStore

vector_db = VectorStore.load("vectorstore")

for chunk_id in [1896, 1897, 1898, 1899]:
    matches = [
        chunk
        for chunk in vector_db.chunks
        if chunk.get("chunk_id") == chunk_id
    ]

    print("\n==============================")
    print("CHUNK:", chunk_id)

    if not matches:
        print("NOT FOUND")
        continue

    chunk = matches[0]

    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:")
    print(chunk["text"][:1200])