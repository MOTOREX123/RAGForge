from utils.ollama_llm import generate_general_answer


def transform_query(question: str) -> list[str]:
    """
    Generate alternative search queries for a user's question.

    The original question is always preserved.
    Ollama generates additional formulations that may improve
    lexical and semantic retrieval.
    """

    prompt = f"""
You are a query rewriting component for a technical-document RAG system.

Original user question:

{question}

Generate exactly 2 alternative search queries.

The alternative queries MUST refer to the SAME concept, entity,
algorithm, model, technique, or topic as the original question.

Rules:

1. Preserve the exact meaning of the original question.
2. Do NOT replace the main technical concept with a related concept.
3. Do NOT introduce a different algorithm, model, technology, or topic.
4. Keep important technical terminology from the original question.
5. You may change wording, sentence structure, or search style.
6. You may convert the question into a concise keyword-oriented search query.
7. Do NOT answer the question.
8. Do NOT add facts that are not present in the original question.
9. Each query must be independently useful for searching technical documents.
10. Return exactly 2 queries.
11. Put each query on its own line.
12. Do not number the queries.
13. Do not use quotation marks.

Example:

Original:
What is overfitting in machine learning?

Good rewrites:
machine learning overfitting definition
definition and characteristics of overfitting in machine learning

Bad rewrite:
underfitting in machine learning

Another example:

Original:
What is a convolutional neural network?

Good rewrites:
convolutional neural network definition
CNN architecture and purpose

Bad rewrite:
recurrent neural network architecture

Now rewrite this question:

{question}
"""

    response = generate_general_answer(prompt)

    queries = [
        line.strip()
        for line in response.splitlines()
        if line.strip()
    ]

    # Remove accidental numbering/bullets.
    cleaned_queries = []

    for query in queries:
        query = query.lstrip("-•* ")
        query = query.removeprefix("1. ").removeprefix("2. ")

        if query:
            cleaned_queries.append(query)

    # Always preserve the original question.
    return [question] + cleaned_queries[:2]
