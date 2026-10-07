import requests

r = requests.get('http://localhost:8000/api/documents', timeout=10)
for d in r.json()['documents']:
    print(f"  - {d['filename']}: {d['chunk_count']} chunks")