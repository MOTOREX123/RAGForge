from utils.conversation import ConversationMemory


def main():

    memory = ConversationMemory(max_turns=2)

    conversation_id = "test-123"

    print("=" * 60)
    print("CONVERSATION MEMORY TEST")
    print("=" * 60)

    memory.add_turn(
        conversation_id,
        "What is overfitting?",
        "Overfitting occurs when a model learns the training data too closely."
    )

    memory.add_turn(
        conversation_id,
        "Why is it a problem?",
        "It can reduce performance on unseen data."
    )

    memory.add_turn(
        conversation_id,
        "How can I prevent it?",
        "Use techniques such as cross-validation and regularization."
    )

    history = memory.get_history(conversation_id)

    print()
    print("Stored turns:")
    print()

    for i, turn in enumerate(history, start=1):

        print(f"Turn {i}")
        print(f"User: {turn['user']}")
        print(f"Assistant: {turn['assistant']}")
        print()

    print(
        f"Total stored turns: {len(history)}"
    )

    assert len(history) == 2

    assert history[0]["user"] == "Why is it a problem?"

    assert history[1]["user"] == "How can I prevent it?"

    print()
    print("PASS: conversation memory works.")


if __name__ == "__main__":
    main()