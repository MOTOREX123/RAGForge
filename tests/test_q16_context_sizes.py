from utils.vectorstore import VectorStore
from utils.router import route_query
from utils.hybrid_retriever import HybridRetriever
from utils.reranker import Reranker
from utils.ollama_llm import generate_ollama_answer


question = "What is underfitting in machine learning?"

vector_db = VectorStore.load("vectorstore")

hybrid_retriever = HybridRetriever(vector_db)
reranker = Reranker()


route = route_query(
    vector_db,
    question,
    k=8,
    threshold=0.50
)

candidates = hybrid_retriever.search(
    question,
    k=10,
    candidate_k=10,
    faiss_results=route["results"]
)

reranked_results = reranker.rerank(
    question,
    candidates,
    top_k=5
)


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


for context_size in [5, 3, 2]:

    print("\n" + "=" * 80)
    print(f"TEST WITH TOP {context_size} CHUNKS")
    print("=" * 80)

    selected_results = reranked_results[:context_size]

    context = build_context(selected_results)

    print("\nCONTEXT:")
    print(context)

    print("\nANSWER:")

    answer = generate_ollama_answer(
        question,
        context
    )

    print(answer)