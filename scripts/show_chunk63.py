import json
import sys

chunks = json.load(open(r'D:\project\New folder (2)\RAGForge\vectorstore\chunks.json', 'r', encoding='utf-8'))

for c in chunks:
    if c['chunk_id'] == 63:
        print(f"Source: {c['source']}")
        print(f"Page: {c['page']}")
        print(f"Chunk ID: {c['chunk_id']}")
        print("Full Text:")
        # Handle encoding for Windows console
        text = c['text'].encode('ascii', 'replace').decode('ascii')
        print(text)
        break