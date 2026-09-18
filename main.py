from pathlib import Path

from utils.vectorstore import VectorStore
from utils.retriever import retrieve_chunks
from utils.router import route_query
# from utils.llm import generate_answer
from utils.ollama_llm import generate_ollama_answer
from utils.web_search import web_search


def main():

    # ==========================================
    # PROJECT PATH
    # ==========================================

    project_root = Path(__file__).resolve().parent

    vectorstore_folder = project_root / "vectorstore"


    # ==========================================
    # LOAD VECTOR STORE
    # ==========================================

    print("=" * 60)
    print("LOADING VECTOR STORE")
    print("=" * 60)

    vector_db = VectorStore.load(str(vectorstore_folder))

    print(f"Loaded chunks: {len(vector_db.chunks)}")
    print(f"Embedding dimension: {vector_db.dimension}")


    # ==========================================
    # CHATBOT
    # ==========================================

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            print("Exiting chatbot...")
            break

        if not question.strip():
            continue

        # ==========================================
        # RETRIEVAL
        # ==========================================

        print("\n" + "=" * 60)
        print("RETRIEVING RELEVANT CHUNKS")
        print("=" * 60)

        route = route_query(
            vector_db,
            question,
            k=8,
            threshold=0.50
        )


        if route["source"] == "local":

            print("\nSource selected: LOCAL DOCUMENTS")

            results = route["results"]

            print("\nRETRIEVED SOURCES")
            print("=" * 60)

            for i, result in enumerate(results, start=1):
                print(f"\n{i}. {result['source']}")
                print(f"   Page: {result['page']}")
                print(f"   Similarity: {result['score']:.4f}")

        elif route["source"] == "web":

            print("\nSource selected: WEB")

            result = web_search(question)

            print("\nANSWER")
            print("=" * 60)
            print(result["answer"])

            print("\nWEB SOURCES")
            print("=" * 60)

            for i, source in enumerate(result["sources"], start=1):
                print(f"\n{i}. {source['title']}")
                print(f"   {source['url']}")

            continue

        # ==========================================
        # GENERATE ANSWER
        # ==========================================

        print("\n" + "=" * 60)
        print("GENERATING ANSWER")
        print("=" * 60)

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

        context = "\n\n".join(context_parts)
        
        answer = generate_ollama_answer(
            question,
            context
        )

        print("\nANSWER:")
        print(answer)


if __name__ == "__main__":
    main()