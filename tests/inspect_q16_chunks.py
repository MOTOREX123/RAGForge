import json

with open("vectorstore/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in chunks:
    if chunk["chunk_id"] in [865, 866]:
        print(f"CHUNK {chunk['chunk_id']} | PAGE {chunk['page']}")
        print("-" * 80)
        print(chunk["text"])
        print("=" * 80)
