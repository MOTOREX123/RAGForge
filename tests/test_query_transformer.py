from utils.query_transformer import transform_query


def main():

    questions = [
        "What is overfitting in machine learning?",
        "What is a convolutional neural network?",
        "What are some applications of deep learning?",
        "What is the OODA loop described in Agentic AI?",
    ]

    for question in questions:

        print()
        print("=" * 70)
        print(f"Original: {question}")
        print("=" * 70)

        queries = transform_query(question)

        for i, query in enumerate(queries, start=1):
            print(f"{i}. {query}")


if __name__ == "__main__":
    main()