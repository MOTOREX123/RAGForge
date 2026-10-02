import json
import sys

chunks = json.load(open(r'D:\project\New folder (2)\RAGForge\vectorstore\chunks.json', 'r', encoding='utf-8'))

for c in chunks:
    text_lower = c['text'].lower()
    if 'depth' in text_lower or 'dfs' in text_lower or 'depth-first' in text_lower:
        print(f"Source: {c['source']}")
        print(f"Page: {c['page']}")
        print(f"Chunk ID: {c['chunk_id']}")
        # Handle encoding
        text = c['text'][:500].encode('ascii', 'ignore').decode('ascii')
        print(f"Text: {text}...")
        print("---")