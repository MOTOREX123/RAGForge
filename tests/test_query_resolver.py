from utils.query_resolver import resolve_query


def main():

    history = [
        {
            "user": "What is overfitting?",
            "assistant": (
                "Overfitting occurs when a model learns "
                "the training data too closely."
            )
        }
    ]

    question = "How can I prevent it?"

    print("=" * 60)
    print("QUERY RESOLUTION TEST")
    print("=" * 60)

    print()
    print("Original question:")
    print(question)

    resolved = resolve_query(
        question,
        history
    )

    print()
    print("Resolved query:")
    print(resolved)

    print()

    assert resolved.strip()

    print("PASS: query resolver returned a query.")


if __name__ == "__main__":
    main()