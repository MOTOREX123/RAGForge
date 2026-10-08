from utils.ollama_llm import generate_answer_with_fallback


def resolve_query(
    question: str,
    history: list[dict],
) -> str:
    """
    Resolve a conversational follow-up question into a
    self-contained search query.

    If there is no conversation history, the original
    question is returned unchanged.
    """

    if not history:
        return question

    history_text = []

    for turn in history:
        history_text.append(
            f"User: {turn['user']}\n"
            f"Assistant: {turn['assistant']}"
        )

    history_text = "\n\n".join(history_text)

    prompt = f"""
You are a query resolution component for a technical-document
RAG system.

Your task is to rewrite the user's latest question into a
self-contained search query using the conversation history.

Conversation history:

{history_text}

Latest user question:

{question}

Rules:

1. Preserve the exact meaning of the user's latest question.
2. Resolve references such as:
   - it
   - this
   - that
   - they
   - the above
   - this method
   - this algorithm
3. Use previous conversation only to resolve missing context.
4. Do NOT answer the question.
5. Do NOT add unrelated information.
6. Do NOT change the technical concept.
7. If the latest question is already self-contained, keep its
   meaning and make only minimal changes.
8. Return exactly ONE search query.
9. Return only the query text.

Examples:

Conversation:
User: What is overfitting?
Assistant: Overfitting occurs when a model learns the training
data too closely.

Latest question:
How can I prevent it?

Output:
How can overfitting in machine learning be prevented?

---

Conversation:
User: What is a convolutional neural network?
Assistant: A CNN is a neural network commonly used for image data.

Latest question:
What are its main layers?

Output:
What are the main layers of a convolutional neural network?

---

Now resolve the latest question.
"""

    try:
        answer, _, _ = generate_answer_with_fallback(prompt, context=None)
    except Exception:
        return question

    if not answer:
        return question

    resolved_query = answer.strip()

    if not resolved_query:
        return question

    return resolved_query