import json
from pathlib import Path


from utils.vectorstore import VectorStore
from utils.router import route_query
from utils.hybrid_retriever import HybridRetriever
from utils.context_selector import select_context
from utils.reranker import Reranker
from utils.ollama_llm import generate_ollama_answer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTORSTORE_FOLDER = PROJECT_ROOT / "vectorstore"


# ============================================================
# Evaluation Dataset
# ============================================================

evaluation_dataset = [
    {
        "question": "What is an agent in artificial intelligence?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [10, 11],
    },
    {
        "question": "What makes an AI agent rational?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [12, 13],
    },
    {
        "question": "What does PEAS stand for in an agent's task environment?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [13],
    },
    {
        "question": "How does breadth-first search explore a search tree?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [25, 26, 28],
    },
    {
        "question": "What is depth-first search and what is one of its limitations?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [29, 32],
    },
    {
        "question": "What is the hill-climbing algorithm?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [35, 36],
    },
    {
        "question": "How does simulated annealing improve on hill climbing?",
        "expected_sources": ["AI & ML DIGITAL NOTES.pdf"],
        "expected_pages": [37, 38],
    },

    {
        "question": "What is a convolutional neural network and what is it useful for?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [34, 95],
    },
    {
        "question": "What type of data pattern is a recurrent neural network designed to handle?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [34],
    },
    {
        "question": "What is the purpose of an activation function in a neural network?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [29, 32],
    },
    {
        "question": "What is backpropagation used for in neural network training?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [39],
    },
    {
        "question": "What is dropout as a deep learning technique?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [62, 63, 64],
    },
    {
        "question": "What types of layers can be used when building neural networks with Keras?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [80],
    },
    {
        "question": "What are some applications of deep learning?",
        "expected_sources": ["DeepLearning.pdf"],
        "expected_pages": [59, 60, 67, 68],
    },

    {
        "question": "What is overfitting in machine learning?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [42],
    },
    {
        "question": "What is underfitting in machine learning?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [42, 62],
    },
    {
        "question": "How is a random forest constructed?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [98, 99],
    },
    {
        "question": "What are linear models used for in machine learning?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [59, 60, 61],
    },
    {
        "question": "What is logistic regression?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [70, 71, 75, 77, 78],
    },
    {
        "question": "What is the basic idea behind Naive Bayes classifiers?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [82, 83, 84],
    },
    {
        "question": "What is cross-validation used for when evaluating machine learning models?",
        "expected_sources": ["Introduction to Machine Learning with Python.pdf"],
        "expected_pages": [266, 267, 268, 269],
    },

    {
        "question": "What is Agentic AI?",
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [1, 2],
    },
    {
        "question": "What does autonomy mean in Agentic AI?",
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [2],
    },
    {
        "question": "How does goal-orientation work in Agentic AI?",
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [3],
    },
    {
        "question": "What is the OODA loop described in Agentic AI?",
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [3],
    },
    {
        "question": "What are the main architectural components of Agentic AI?",
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [4, 5],
    },
    {
        "question": (
            "How do memory, planning, execution, and tool integration "
            "work together in an Agentic AI architecture?"
        ),
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [4, 5],
    },
    {
        "question": (
            "What are the Tool-Using Agent, Multi-Agent Collaboration, "
            "and Reflection design patterns?"
        ),
        "expected_sources": ["IntroductiontoAgenticAI.pdf"],
        "expected_pages": [6, 7],
    },
]


# ============================================================
# Helpers
# ============================================================

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

# =========================================================
# put this above main(), after build_context()
# =========================================================

def save_results(results):
    output_path = (
    PROJECT_ROOT
    / "tests"
    / "citation_evaluation_results.json"
)

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False,
        )

# ============================================================
# Main Evaluation
# ============================================================

def main():

    print("=" * 70)
    print("END-TO-END ANSWER EVALUATION")
    print("=" * 70)

    print("\nLoading vector store...")

    vector_db = VectorStore.load(
        str(VECTORSTORE_FOLDER)
    )

    print(f"Loaded chunks: {len(vector_db.chunks)}")

    print("\nBuilding hybrid retriever...")

    hybrid_retriever = HybridRetriever(vector_db)

    print("Hybrid retriever ready.")

    print("\nLoading reranker...")

    reranker = Reranker()

    print("Reranker ready.")

    results = []

    total = len(evaluation_dataset)

    for index, item in enumerate(evaluation_dataset, start=1):

        question = item["question"]

        print("\n" + "-" * 70)
        print(f"[{index}/{total}] {question}")

        route = route_query(
            vector_db,
            question,
            k=8,
            threshold=0.50,
        )

        if route["source"] != "local":

            print(f"Route: {route['source']}")
            print("Skipping answer generation.")

            results.append({
                "question": question,
                "route": route["source"],
                "answer": None,
                "citations": [],
                "generation_error": None,
                "expected_sources": item["expected_sources"],
                "expected_pages": item["expected_pages"],
            })

            save_results(results)

            continue

        candidates = hybrid_retriever.search(
            question,
            k=10,
            candidate_k=10,
            faiss_results=route["results"],
        )

        reranked_results = reranker.rerank(
            question,
            candidates,
            top_k=5
        )

        selected_results = select_context(
            reranked_results,
            max_chunks=3,
            min_score=0.0
        )

        context = build_context(
            selected_results
        )

        try:
            answer = generate_ollama_answer(
                question,
                context,
            )

            generation_error = None

        except Exception as first_exc:
            print(f"Generation failed on first attempt: {first_exc}")
            print("Retrying once...")

        try:
            answer = generate_ollama_answer(
                question,
                context,
            )

            generation_error = None
            print("Retry succeeded.")

        except Exception as second_exc:
            answer = None
            generation_error = str(second_exc)

            print(f"Generation failed after retry: {second_exc}")

        citations = []

        for result in selected_results:
            citations.append({
                "source": result["source"],
                "page": result.get("page"),
                "score": result.get("rerank_score"),
            })

        print(f"Route: {route['source']}")
        print(f"Answer: {answer}")

        results.append({
            "question": question,
            "route": route["source"],
            "answer": answer,
            "context": context,
            "citations": citations,
            "generation_error": generation_error,
            "expected_sources": item["expected_sources"],
            "expected_pages": item["expected_pages"],
        })

        save_results(results)

    

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(f"\nQuestions evaluated: {total}")
    print("Results saved to:")
    print(
        PROJECT_ROOT
        / "tests"
        / "answer_evaluation_results.json"
    )

if __name__ == "__main__":
    main()