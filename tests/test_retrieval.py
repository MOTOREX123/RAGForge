import requests
import json

payload = {'message': 'What is agentic AI?', 'conversation_id': None}
r = requests.post('http://localhost:8000/api/chat', json=payload, timeout=60)
print('Status:', r.status_code)
data = r.json()
print('Route:', data['route'])
print('Answer preview:', data['answer'][:200])
print('Citations:')
for c in data['citations']:
    print(f'  - {c["source"]} p.{c["page"]} score={c["score"]:.2f}')