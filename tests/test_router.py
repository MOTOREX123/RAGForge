from utils.vectorstore import VectorStore
from utils.router import route_query


vectorstore = VectorStore.load("vectorstore")


questions = [
    "What is supervised learning?",
    "What is the latest version of Python?",
    "Who is Cristiano Ronaldo?",
    "What is overfitting in machine learning?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    route = route_query(
        vectorstore,
        question,
        k=5,
        threshold=0.45
    )

    print("SOURCE:", route["source"])
    print("REASON:", route["reason"])

    if route["source"] == "local":
        print("LOCAL RESULTS:", len(route["results"]))