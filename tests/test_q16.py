import json
from pathlib import Path
import sys
sys.path.insert(0, r'D:\project\New folder (2)\RAGForge')

from utils.vectorstore import VectorStore
from utils.router import route_query
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker
from utils.context_selector import select_context
from utils.ollama_llm import generate_ollama_answer

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))

# Load vector store
PROJECT_ROOT = Path(__file__).resolve().parent
VECTORSTORE_FOLDER = PROJECT_ROOT / "vectorstore"

vector_db = VectorStore.load(str(VECTORSTORE_FOLDER))

question = "What is underfitting?"

route = route_query(vector_db, question, k=8, threshold=0.50)

hybrid_retriever = HybridRetriever(vector_db)
candidates = hybrid_retriever.search(
    question,
    k=10,
    candidate_k=10,
    faiss_results=route["results"]
)

reranker = Reranker()
results = reranker.rerank(question, candidates, top_k=5)

selected_results = select_context(results, max_chunks=3, min_score=0.0)

def build_context(results):
    context_parts = []
    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"""
[{i}]
Source: {result['source']}
Page: {result['page']}

{result['text']}
"""
        )
    return "\n\n".join(context_parts)

context = build_context(selected_results)

print("=" * 60)
print("CONTEXT SENT TO OLLAMA")
print("=" * 60)
safe_print(context)

print("\n" + "=" * 60)
print("OLLAMA ANSWER")
print("=" * 60)

try:
    answer = generate_ollama_answer(question, context)
    safe_print(answer)
except Exception as e:
    print(f"Ollama error: {e}")